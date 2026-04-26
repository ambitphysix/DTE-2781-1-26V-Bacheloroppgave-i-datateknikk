from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, EqualTo


# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField("Brukernavn", validators=[DataRequired()])
    password = PasswordField("Passord", [validators.Length(min=3, max=255)])
    password_confirm = PasswordField(
        "Bekreft passord", validators=[DataRequired(), EqualTo("password")]
    )


# Form for user login
class LoginForm(FlaskForm):
    username = StringField("Brukernavn", validators=[DataRequired()])
    password = PasswordField("Passord", validators=[DataRequired()])
    submit = SubmitField("Logg inn")
