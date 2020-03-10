"""Define DB Models."""

from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __talbename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String(20),
                           nullable=False,
                           unique=False)
    last_name = db.Column(db.String(20),
                          nullable=False,
                          unique=False)
    email = db.Column(db.String(40),
                      nullable=False,
                      unique=True)
    password = db.Column(db.String(200),
                         nullable=False,
                         unique=False,
                         primary_key=False)
    cash = db.Column(db.Float,
                     nullable=False,
                     unique=False,
                     default=10000.00)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        """Object representation."""
        return "<User {}>".format(self.first_name)


class Transaction(db.Model):
    """Model for transaction information."""

    __talbename__ = "transactions"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        nullable=False,
                        unique=False)
    symbol = db.Column(db.String(10),
                       nullable=False,
                       unique=False)
    shares = db.Column(db.Integer,
                       nullable=False,
                       unique=False)

    def __repr__(self):
        """Object representation."""
        return "<Transaction {}>".format(self.id)


class History(db.Model):
    """Model for user's transaction history."""

    __talbename__ = "history"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        nullable=False,
                        unique=False)
    symbol = db.Column(db.String(10),
                       nullable=False,
                       unique=False)
    shares = db.Column(db.Integer,
                       nullable=False,
                       unique=False)
    cost = db.Column(db.Float,
                     nullable=False,
                     unique=False)
    transaction_time = db.Column(db.DateTime,
                                 nullable=False,
                                 unique=False,
                                 default=datetime.utcnow)

    def __repr__(self):
        """Object representation."""
        return "<History {}>".format(self.id)


class ResetPassword(db.Model):
    """Model for password reset."""

    __talbename__ = "reset-password"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(40),
                      nullable=False,
                      unique=True)
    token = db.Column(db.String,
                      nullable=False,
                      unique=False)
    expiration_time = db.Column(db.DateTime,
                                unique=False,
                                nullable=False,
                                default=datetime.utcnow)

    def __repr__(self):
        """Object representation."""
        return "<ResetPassword {}>".format(self.id)
