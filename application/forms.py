from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, NumberRange


class SignInForm(FlaskForm):
    """SignIn form"""

    email = StringField("Email", validators=[DataRequired(message="Please provide your email."),
                                             Email(message="Please enter a valid email address.")])
    password = PasswordField("Password", validators=[
                             DataRequired(message="Please provide your password.")])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """Registration form"""

    first_name = StringField("first_name", validators=[
                             DataRequired(message="Please proivde your first name.")])
    last_name = StringField("last_name", validators=[
                            DataRequired(message="Please proivde your last name.")])
    email = StringField("email", validators=[DataRequired(message="Please provide your email address."),
                                             Email(message="Please provide a valid email address.")])
    password = PasswordField("password", validators=[DataRequired(message="Please provide a password."),
                                                     Length(
                                                         min=5, message="Password must contain more than 5 characters."),
                                                     Regexp("^(?=.*[A-Z]+)(?=.*[!@#$&*])(?=.*[0-9]+)(?=.*[a-z]+).{5,}$", message="Password must contain an uppercase, digit & special character.")])
    confirm_password = PasswordField("confirm_password", validators=[DataRequired(message="Please provide password again."),
                                                                     EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Register")


class BuyForm(FlaskForm):
    """Class To Buy Form"""

    symbol = StringField("symbol", validators=[
                         DataRequired(message="Must provide a symbol")])
    shares = IntegerField("Number of shares", validators=[DataRequired(message="Please provide number of shares."),
                                                          NumberRange(min=1, max=100, message="Shares must be between 1 and 100.")])
    submit = SubmitField("Buy")


class SellForm(FlaskForm):
    """Sell Form"""

    symbol = SelectField("Symbol", validators=[
                         DataRequired(message="Please select a stock.")])
    shares = IntegerField("Number of shares", validators=[DataRequired(message="Please provide number of shares."),
                                                          NumberRange(min=1, max=100, message="Shares must be between 1 and 100.")])
    submit = SubmitField("Sell")


class QuoteForm(FlaskForm):
    """Quote Form"""

    symbol = StringField("symbol", validators=[
                         DataRequired(message="Must provide a symbol")])
    submit = SubmitField("Quote")


class ResetPasswordForm(FlaskForm):
    """Reset Password Form"""

    email = StringField("Email", validators=[DataRequired(message="Please provide your email."),
                                             Email(message="Please enter a valid email address.")])
    submit = SubmitField("Submit")


class UpdatePasswordForm(FlaskForm):
    """Update Password"""

    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(message="Please provide a password."),
                                                     Length(
                                                         min=5, message="Password must contain more than 5 characters."),
                                                     Regexp("^(?=.*[A-Z]+)(?=.*[!@#$&*])(?=.*[0-9]+)(?=.*[a-z]+).{5,}$", message="Password must contain an uppercase, digit & special character.")])
    confirm_password = PasswordField("confirm_password", validators=[DataRequired(message="Please provide password again."),
                                                                     EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Update")
