from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField,
    IntegerField,
    validators,
    EmailField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length

# Form for user profile edit
class ProfileEditForm(FlaskForm):
    picture = FileField("Profile Picture")
    firstname = StringField("First Name")
    lastname = StringField("Last Name")
    submit = SubmitField("Update Profile")


# Form for registration
class RegistrationForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    email = EmailField(
        "Email",
        [
            validators.Length(min=5, max=255),
            Email(message="Please input a valid email"),
        ],
    )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", [validators.Length(min=3, max=255)])
    password_confirm = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    file = FileField("Profile Picture", validators=[Optional()])
    surename = StringField('Surename')


# Form for user login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class GetUser(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    value = StringField("Value", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    reason = StringField("Reason", validators=[DataRequired()])
    who = StringField("Who", validators=[DataRequired()])
    page = IntegerField("Page", validators=[DataRequired()])
    order = IntegerField("Order", validators=[DataRequired()])


class GetNewsletter(FlaskForm):
    newsletter = StringField("Newsletter", validators=[DataRequired()])


# Form for searching for usernames
class SearchUsernames(FlaskForm):
    search_term = StringField(
        "Search Friends", validators=[DataRequired(), Length(min=3, max=100)]
    )
