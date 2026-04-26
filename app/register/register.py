from flask import Blueprint, render_template, flash, redirect, url_for
from app.UserForm import RegistrationForm
from app.db import UsersDB
from werkzeug.security import generate_password_hash

BP = Blueprint(
    "register", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_confirm = form.password_confirm.data

        if password != password_confirm:
            flash("Passwords do not match. Please try again.", category = "warning")
            return redirect(url_for("register.register"))

        with UsersDB() as db:
            usernameCheck = db.check_user(username)
            if usernameCheck[next(iter(usernameCheck))]:
                flash(
                    "Brukernavnet er allerede i bruk. Vennligst velg et annet",
                    "error",
                )
                return redirect(url_for("register.register"))
            else:
                db.add_new_user(username, generate_password_hash(password))
                flash("Brukeren ble opprettet.", category = "success")
                return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)