"""Initialize app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from flask_login import LoginManager
from flask_assets import Environment, Bundle


# Globally accessible libraries
db = SQLAlchemy()
mail = Mail()
sess = Session()
login_manager = LoginManager()
env = Environment()

# Bundle js and css files
css_bundle = Bundle("css/*.css",
                    filters="cssmin",
                    output="build/css/all_styles.css")

js_bundle = Bundle("js/jquery-3.3.1.min.js",
                   "js/bootstrap.min.js",
                   "js/popper.min.js",
                   "js/myscript.js",
                   filters="jsmin",
                   output="build/js/all_js.js")


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Derive configuration values
    app.config.from_object("config.Config")

    # Initialize plugins
    db.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    login_manager.init_app(app)
    env.init_app(app)

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

        # Register and build assets
        env.register("all_styles", css_bundle)
        env.register("all_js", js_bundle)
        css_bundle.build()
        js_bundle.build()

        return app
