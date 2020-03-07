"""application/init."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from dateutil import tz
from ..helpers import login_required, lookup, usd, sorry
from ..models import User, Transaction, History
from ..forms import QuoteForm, BuyForm, SellForm
from .. import db


# Set up a blueprint
loggedin_bp = Blueprint("loggedin_bp", __name__,
                        template_folder="templates")


# Add custom filter
loggedin_bp.add_app_template_filter(usd)


@loggedin_bp.route("/", methods=["GET"])
@login_required
def home():
    """Show portfolio of stocks."""
    grand_total = 0

    # List of transactions of a user
    # transactions = Transaction.query.filter_by(
    #     user_id=session["user_id"]).order_by(Transaction.symbol.asc()).all()

    transactions = Transaction.query.filter_by(
        user_id=session["user_id"]).all()

    if transactions:
        for transaction in transactions:
            # Get information about a stock
            info = lookup(transaction.symbol)
            if info:
                total_per_stock = transaction.shares * info["price"]
                grand_total += total_per_stock

                # Add new properties to transaction object
                transaction.name = info["name"]
                transaction.price = info["price"]
                transaction.total = total_per_stock

    # Check user's available balance
    current_cash = (User.query.filter_by(id=session["user_id"]).first()).cash
    grand_total += current_cash

    # Render index template
    return render_template("index.html", transactions=transactions, current_cash=current_cash, grand_total=grand_total)


@loggedin_bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    form = QuoteForm()

    if form.validate_on_submit():
        # Get information for given symbol
        info = lookup(request.form.get("symbol"))

        # Show information
        if info:
            return render_template('quote.html', info=info)

        # Notify for invalid symbol
        else:
            return sorry("invalid symbol")

    return render_template("quote.html", form=form)


@loggedin_bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    form = BuyForm()

    # If GET request sent from 'sell this' button
    symbol = request.args.get("symbol")

    # When form is validated
    if form.validate_on_submit():

        # Check if shares are negative
        if request.form.get("shares")[0] == "-":
            return sorry("shares must not be negative", 400)

        # Check if shares are float
        elif not request.form.get("shares").replace(".", "", 1).isdigit():
            return sorry("shares must not be fractional", 400)

        # Check if shares are non-numeric
        elif not request.form.get("shares").isdigit():
            return sorry("shares must be numeric", 400)

        # Get data for given symbol
        info = lookup(request.form.get("symbol"))

        # Data available
        if info:

            # Calculate new cost
            new_cost = int(request.form.get("shares")) * float(info["price"])

            # Check user's available balance
            current_balance = (User.query.filter_by(
                id=session["user_id"]).first()).cash

            # Check user's affordability
            if new_cost > current_balance:
                return sorry("you don't have enough cash")

            # Calculate new cash
            updated_cash = current_balance - new_cost

            # Check if user has purchased same stock before
            prev_purchase = Transaction.query.filter_by(user_id=session["user_id"],
                                                        symbol=info["symbol"]).first()

            if prev_purchase:
                """Update shares if user has already purchased a stock before"""

                # Get the current number of shares
                current_shares = prev_purchase.shares

                # Calculate updated shares
                updated_shares = current_shares + \
                    int(request.form.get("shares"))

                # Update transactions table
                prev_purchase.shares = updated_shares

                # Update users table
                user_info = User.query.filter_by(id=session["user_id"]).first()
                user_info.cash = updated_cash

            else:
                """Insert data into transactions table"""

                # Insert transactions table
                new_purchase = Transaction(user_id=session["user_id"],
                                           symbol=info["symbol"],
                                           shares=request.form.get("shares"))
                db.session.add(new_purchase)

                # Update cash of users table
                user_info = User.query.filter_by(id=session["user_id"]).first()
                user_info.cash = updated_cash

            # Update history table
            transaction_history = History(user_id=session["user_id"],
                                          symbol=info["symbol"],
                                          shares=request.form.get("shares"),
                                          cost=new_cost)
            db.session.add(transaction_history)
            db.session.commit()
            db.session.close()

        # Notify user for invalid symbol
        else:
            return sorry("invalid symbol")

        # Display flash message and redirect to homepage
        flash("Congrats! You've successfully bought!")
        return redirect(url_for(".home"))

    # If user clicks the buy button
    return render_template("buy.html", form=form, symbol=symbol)


@loggedin_bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares."""
    form = SellForm()

    # If GET request received from 'buy this' button
    symbol = request.args.get("symbol")

    # Insert choices
    if symbol:
        form.symbol.choices = [(symbol, symbol)]
    else:
        form.symbol.choices = [(transaction.symbol, transaction.symbol) for transaction in Transaction.query.filter_by(
            user_id=session["user_id"]).order_by(Transaction.symbol.asc()).all()]

    if form.validate_on_submit():
        """If validation is successful"""

        # Number of shares of selected stock
        selected_stock = Transaction.query.filter_by(
            user_id=session["user_id"], symbol=request.form.get("symbol")).first()

        # Restrict user from selling more shares than s/he has
        if int(request.form.get("shares")) > selected_stock.shares:
            return sorry("you don't have enough shares to sell", 400)

        # Get information about this stock
        info = lookup(request.form.get("symbol"))

        # Current selling price
        selling_price = info["price"] * int(request.form.get("shares"))

        # Update the cash for the user
        current_user = User.query.filter_by(id=session["user_id"]).first()
        current_user.cash += selling_price

        # DELETE row if user wills to sell all shares of a stock
        if (int(request.form.get("shares")) == selected_stock.shares):
            db.session.delete(selected_stock)

        # Update number of shares
        else:
            selected_stock.shares -= int(request.form.get("shares"))

        # Update history table
        transaction_history = History(user_id=session["user_id"],
                                      symbol=info["symbol"],
                                      shares=int(
                                          request.form.get("shares")) * -1,
                                      cost=selling_price)
        db.session.add(transaction_history)
        db.session.commit()

        # Send the flash message to homepage
        flash("Congrats! You've successfully sold!")

        db.session.close()

        # Return to homepage
        return redirect(url_for(".home"))

    return render_template("sell.html", form=form)


@loggedin_bp.route("/history")
@login_required
def history():
    """
    Show history of transactions.

    Transaction time processed using the following link.
    (https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime).
    """
    current_timezone = tz.gettz("UTC")
    desired_timezone = tz.gettz("Asia/Dhaka")

    # Get history data
    transactions = History.query.filter_by(user_id=session["user_id"]).order_by(
        History.transaction_time.desc()).all()

    if transactions:
        """Travarse all transactions"""

        for transaction in transactions:

            # Get information for symbol
            info = lookup(transaction.symbol)

            # Cost to buy or sell shares
            transaction.cost = abs(info["price"] * transaction.shares)

            # Tell the datetime object that the default timezoe is UTC
            transaction.transaction_time.replace(tzinfo=current_timezone)

            # Convert to local time
            local_time = transaction.transaction_time.astimezone(
                desired_timezone)

            # Format time
            formatted_local_time = local_time.strftime("%d-%m-%Y %I:%M:%S %p")
            transaction.transaction_time = formatted_local_time

    return render_template("history.html", transactions=transactions)
