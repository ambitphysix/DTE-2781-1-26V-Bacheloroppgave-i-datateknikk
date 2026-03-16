from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user
from app.UserForm import LoginForm
from app.user import User


BP = Blueprint(
    "auth", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        value = User.login(username, password)
        if value == "success":
            flash("Logged in successfully!", category="success")
            return redirect(url_for("index.index"))
        elif value == "flagged":
            flash(
                "Your account has been flagged. Please contact support.",
                category="error",
            )
        else:
            flash(
                "Incorrect username, password or user is not verified", category="error"
            )
    return render_template("login.html", form=form)


@BP.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("index.index"))
