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
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        value = User.login(username, password)
        if value == "success":
            flash("Logget in", category = "success")
            return redirect(url_for("index.index"))
        else:
            flash("Ugydlig kombinasjon av brukernavn og passord", category = "warning")
    return render_template("login.html", form=form)


@BP.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Du har blitt logget ut.", "success")
    return redirect(url_for("index.index"))
