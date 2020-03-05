"""This blueprint contains all functions to authenticate users."""

import os
import secrets
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_mail import Message
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from ..helpers import sorry
from ..forms import SignInForm, RegistrationForm, ResetPasswordForm, UpdatePasswordForm
from ..models import User, ResetPassword
from .. import db, mail

# Set up a Blueprint
auth_bp = Blueprint("auth_bp", __name__,
                    template_folder="templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    form = RegistrationForm()

    # When form has been validated
    if form.validate_on_submit():

        # Clear any previous session
        session.clear()

        # To Do: Validatoin for existing emails using wtform

        # Check if email alrady exists
        user_exists = User.query.filter_by(
            email=request.form.get("email")).first()
        if user_exists:
            return sorry("someone's already using that email")

        # Insert data into database
        new_user = User(first_name=request.form.get("first_name"),
                        last_name=request.form.get("last_name"),
                        email=request.form.get("email"))
        new_user.pwd_generator(request.form.get("password"))
        db.session.add(new_user)
        db.session.commit()

        # Save user id to the sesssion
        session["user_id"] = new_user.id

        # Save email to the sesssion
        session["first_name"] = request.form.get("first_name")

        # Send the flash message to homepage
        flash("Congrats!")

        db.session.close()

        # Redirect user to home page
        return redirect(url_for("home"))
        # return "Return to homepage"

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    form = SignInForm()

    # When form has been validated
    if form.validate_on_submit():

        # Clear any previous session
        session.clear()

        """
            To Do: Validatoin for incorrect password using wtform
        """

        # Find email
        user_exists = (User.query.filter_by(
            email=request.form.get("email"))).first()

        # Check email
        if not user_exists:
            return sorry("your email is incorrenct")

        # Check password
        if not user_exists.pwd_checker(request.form.get("password")):
            return sorry("your password is incorrenct")

        # Remember which user has logged in
        session["user_id"] = user_exists.id

        # Save email to the sesssion
        session["first_name"] = user_exists.first_name

        # Send the flash message to homepage
        flash("Welcome!")

        # Redirect user to home page
        return redirect(url_for("loggedin_bp.home"))

    return render_template('login.html', form=form)


@auth_bp.route("/logout")
def logout():
    """Log user out."""
    session.clear()

    # Redirect user to login form
    return redirect(url_for("loggedin_bp.home"))


@auth_bp.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    """Reset Password."""
    form = ResetPasswordForm()

    if form.validate_on_submit():
        """When the form is validated"""

        # Check if provided email is registered
        user_exists = User.query.filter_by(
            email=request.form.get("email")).first()

        if user_exists:

            # Generate 32 byte token
            token = secrets.token_urlsafe(32)

            # Generate reset password link
            action_url = "https://finance-stocks.herokuapp.com/req_to_change_password?token=" + token

            # Check if previous token exists
            token_exists = ResetPassword.query.filter_by(
                email=request.form.get("email")).first()

            if token_exists:
                """Update the previous token and expiration time"""

                token_exists.token = token
                token_exists.expiration_time = datetime.utcnow() + timedelta(hours=24)
                db.session.commit()

            else:
                """Insert new token and expiration time"""

                new_token = ResetPassword(email=request.form.get("email"),
                                          token=token,
                                          expiration_time=datetime.utcnow() + timedelta(hours=24))
                db.session.add(new_token)
                db.session.commit()

            # Send mail
            try:
                msg = Message("Reset Password", sender=os.environ.get("MAIL_ID"),
                              recipients=[request.form.get("email")])
                msg.html = render_template("reset_email.html",
                                           name=user_exists.first_name,
                                           action_url=action_url)
                mail.send(msg)
                return render_template("resend.html")

            except:
                return sorry("we could not send the mail to you. Please relaod or request again", 500)
            # except Exception as e:
            #     return str(e)

        # The requested email does not exists
        else:
            try:
                msg = Message("Reset Password", sender=os.environ.get("MAIL_ID"),
                              recipients=[request.form.get("email")])
                msg.html = render_template("reset_email.html")
                mail.send(msg)
                return render_template("resend.html")

            except:
                return sorry("we could not send the mail to you. Please relaod or request again", 500)

    db.session.close()
    return render_template("reset.html", form=form)


@auth_bp.route("/req_to_change_password", methods=["GET"])
def req_to_change_password():
    """Token Validation."""
    token_exists = ResetPassword.query.filter_by(
        token=request.args.get("token")).first()

    if token_exists:
        # When the token is valid
        if datetime.utcnow() <= token_exists.expiration_time:
            return redirect(url_for(".update_password", email=token_exists.email))

        else:
            return sorry("this token has expired.", 400)

    else:
        return sorry("the token does not exist.", 400)


@auth_bp.route("/update_password", methods=["GET", "POST"])
def update_password():
    """Update user's password."""
    form = UpdatePasswordForm()

    """
        email is received via GET method from url_for(req_to_change_password).
        This email is attached to the form as a hidden field. So, when we
        submit the form, we can access the email address via
        request.form.get(email) as the form wiill be submitted via POST method.
    """
    email = request.args.get("email")

    if form.validate_on_submit():
        # Update password
        user = User.query.filter_by(email=request.form.get("email")).first()
        user.hash = generate_password_hash(request.form.get('password'))

        # Delete token
        current_token = ResetPassword.query.filter_by(
            email=request.form.get("email")).first()
        db.session.delete(current_token)
        db.session.commit()

        # save id in session
        session["user_id"] = user.id
        session["first_name"] = user.first_name

        db.session.close()
        return redirect(url_for("home"))

    else:
        return render_template("update_password.html", form=form, email=email)
