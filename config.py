import os
from tempfile import mkdtemp

class Config:
    """Set Flask configuration vars."""

    # General config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TEMPLATES_AUTO_RELOAD = True

    # Database
    database_file = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    DEBUG = True
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_ID")
    MAIL_PASSWORD = os.environ.get("MAIL_PASS")
    
    # Session
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"