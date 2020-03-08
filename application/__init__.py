"""application/init."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session


# Globally accessible libraries
db = SQLAlchemy()
mail = Mail()
sess = Session()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Derive configuration values
    app.config.from_object("config.Config")

    # Initialize plugins
    db.init_app(app)
    mail.init_app(app)
    sess.init_app(app)

    with app.app_context():

        # Import Models
        from .models import User, Transaction, History, ResetPassword

        # Create tables for models
        db.create_all()

        # Include blueprints
        from .auth import auth_routes
        from .loggedin import loggedin_routes
        from .landing import landing_routes

        # Register blueprints
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(loggedin_routes.loggedin_bp)
        app.register_blueprint(landing_routes.landing_bp)

        return app
