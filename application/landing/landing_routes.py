"""Defines the functionalities of the landing page."""

from flask import Blueprint, render_template, redirect, url_for, flash

# Set up blueprint
landing_bp = Blueprint("landing_bp", __name__, template_folder="templates")


@landing_bp.route("/")
def home():
    """The landing page."""
    flash("You may try email: test and password: 123!")
    return redirect(url_for("auth_bp.login"))


@landing_bp.route("/faq")
def faq():
    """Display the faq page."""
    return render_template("faq.jinja2")
