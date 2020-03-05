from . import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """Model for user information"""

    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    cash = db.Column(db.Float, nullable=False, default=10000.00)

    # Methods
    def pwd_generator(self, pwd):
        self.hash = generate_password_hash(pwd)

    def pwd_checker(self, pwd):
        return check_password_hash(self.hash, pwd)

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, cash={self.cash})>"


class Transaction(db.Model):
    """Model for transaction information"""

    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, symbol={self.symbol}, shares={self.shares})>"


class History(db.Model):
    """Model for user's transaction history"""

    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    transaction_time = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, symbol={self.symbol}, shares={self.shares}, cost={self.cost}, transaction_time={self.transaction_time})>"


class ResetPassword(db.Model):
    """Model for password reset"""

    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    token = db.Column(db.String, nullable=False)
    expiration_time = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ResetPassword(id={self.id}, token={self.token}, expiration_time={self.expiration_time})>"
