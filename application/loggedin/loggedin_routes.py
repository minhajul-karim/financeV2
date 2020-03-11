"""Defines functinalities of logged in state."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from dateutil import tz
from ..helpers import lookup, usd, sorry
from ..models import User, Transaction, History
from ..forms import QuoteForm, BuyForm, SellForm
from .. import db


# Set up a blueprint
loggedin_bp = Blueprint("loggedin_bp", __name__,
                        template_folder="templates")


# Add custom filter
loggedin_bp.add_app_template_filter(usd)


@loggedin_bp.route("/portfolio", methods=["GET"])
@login_required
def portfolio():
    """Show portfolio of stocks."""
    try:
        grand_total = 0

        # List of transactions of a user
        transactions = Transaction.query.filter_by(
            user_id=current_user.id).order_by(Transaction.symbol.asc()).all()

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
        current_cash = current_user.cash
        grand_total += current_cash

        # Render index template
        flash(f"Welcome {current_user.first_name}!")
        return render_template("portfolio.jinja2",
                               transactions=transactions,
                               current_cash=current_cash,
                               grand_total=grand_total)

    except:
        return sorry("something is wrong! Please reload.")


@loggedin_bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    quote_form = QuoteForm()

    if request.method == "POST":
        if quote_form.validate_on_submit():
            symbol = quote_form.symbol.data
            # Get information for given symbol
            info = lookup(symbol)
            if info:
                return render_template('quote.jinja2', info=info)
            else:
                flash("Sorry! Invalid symbol.")
                return redirect(url_for(".quote"))

    return render_template("quote.jinja2", form=quote_form)


@loggedin_bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # If GET request sent from 'sell this' button
    selected_symbol = request.args.get("symbol")

    buy_form = BuyForm()
    if request.method == "POST":
        if buy_form.validate_on_submit():
            symbol = buy_form.symbol.data
            shares = buy_form.shares.data

            # Get data for given symbol
            info = lookup(symbol)
            if info:
                new_cost = shares * float(info["price"])
                current_balance = (User.query.filter_by(
                    id=current_user.id).first()).cash
                if new_cost > current_balance:
                    flash("You don't have enough cash!")
                    return redirect(url_for(".buy"))

                # Calculate new cash after successful purchase
                updated_cash = current_balance - new_cost

                # Check if user has purchased same stock before
                prev_purchase = Transaction.query.filter_by(user_id=current_user.id,
                                                            symbol=info["symbol"]).first()
                if prev_purchase:
                    current_shares = prev_purchase.shares
                    updated_shares = current_shares + shares

                    # Update transactions table
                    prev_purchase.shares = updated_shares

                    # Update users table
                    user_info = User.query.filter_by(
                        id=current_user.id).first()
                    user_info.cash = updated_cash

                else:
                    new_purchase = Transaction(user_id=current_user.id,
                                               symbol=info["symbol"],
                                               shares=request.form.get("shares"))
                    db.session.add(new_purchase)

                    # Update cash of users table
                    user_info = User.query.filter_by(
                        id=current_user.id).first()
                    user_info.cash = updated_cash

                # Update history table
                transaction_history = History(user_id=current_user.id,
                                              symbol=info["symbol"],
                                              shares=request.form.get(
                                                  "shares"),
                                              cost=new_cost)
                db.session.add(transaction_history)
                db.session.commit()
                db.session.close()

            else:
                flash("Invalid symbol!")
                return redirect(url_for(".buy"))

            flash("Congrats! You've successfully purchased!")
            return redirect(url_for(".portfolio"))

    return render_template("buy.jinja2", form=buy_form, symbol=selected_symbol)


@loggedin_bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares."""
    sell_form = SellForm()

    # If GET request received from 'buy this' button
    selected_symbol = request.args.get("symbol")

    # Insert choices
    if selected_symbol:
        sell_form.symbol.choices = [(selected_symbol, selected_symbol)]
    else:
        sell_form.symbol.choices = [(transaction.symbol, transaction.symbol) for transaction in Transaction.query.filter_by(
            user_id=current_user.id).order_by(Transaction.symbol.asc()).all()]

    if request.method == "POST":
        if sell_form.validate_on_submit():
            symbol = sell_form.symbol.data
            shares = sell_form.shares.data

            selected_stock = Transaction.query.filter_by(
                user_id=current_user.id, symbol=symbol).first()

            if shares > selected_stock.shares:
                flash("Sorry! you don't have enough shares to sell.")
                return redirect(url_for(".sell"))

            # Get information about this stock
            info = lookup(request.form.get("symbol"))
            selling_price = info["price"] * shares

            # Update the cash for the user
            active_user = User.query.filter_by(id=current_user.id).first()
            active_user.cash += selling_price

            # Update Transaction table if user wills to sell all shares of a
            # stock
            if (shares == selected_stock.shares):
                db.session.delete(selected_stock)
            else:
                selected_stock.shares -= shares

            # Update history table
            transaction_history = History(user_id=current_user.id,
                                          symbol=info["symbol"],
                                          shares=shares * -1,
                                          cost=selling_price)
            db.session.add(transaction_history)
            db.session.commit()
            db.session.close()

            flash("Congrats! You've successfully sold!")
            return redirect(url_for(".portfolio"))

    return render_template("sell.jinja2", form=sell_form)


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
    transactions = History.query.filter_by(user_id=current_user.id).order_by(
        History.transaction_time.desc()).all()
    if transactions:
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

    return render_template("history.jinja2", transactions=transactions)
