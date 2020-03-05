"""application/landing/landing_routes."""

from flask import Blueprint, render_template

# Set up blueprint
landing_bp = Blueprint("landing_bp", __name__, template_folder="templates")


@landing_bp.route("/faq")
def faq():
    """Display the faq page."""
    return render_template("faq.html")
