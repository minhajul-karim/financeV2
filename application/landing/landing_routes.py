"""Defines the functionalities of the landing page."""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user
from ..forms import LoginForm
from ..models import User

# Set up blueprint
landing_bp = Blueprint("landing_bp", __name__, template_folder="templates")


@landing_bp.route("/", methods=["GET", "POST"])
def home():
    """
    Home Page.

    GET: Serve Home page.
    POST: If submitted credentials of Log-in form are valid, redirect user to the logged-in homepage.
    """
    if current_user.is_authenticated:
        # Bypass if user is logged in
        return redirect(url_for("loggedin_bp.portfolio"))

    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password=password):
                login_user(user)
                next_page = request.args.get("next")
                # To Do: Need to check the next_page url if its safe
                return redirect(next_page or url_for("loggedin_bp.portfolio"))
        flash("Invalid email/password combination")
        return redirect(url_for(".home"))

    return render_template("home.jinja2", form=login_form)


@landing_bp.route("/faq")
def faq():
    """Display the faq page."""
    return render_template("faq.jinja2")
