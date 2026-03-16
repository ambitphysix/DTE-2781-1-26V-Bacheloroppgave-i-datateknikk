from flask import Blueprint, flash, redirect, url_for, render_template
from flask_mail import Mail, Message
from app.UserForm import RegistrationForm
from app.db.UsersDB import UsersDB
from config import config
from app import application as app
from app.app import encrypt_email
from werkzeug.security import generate_password_hash


app.config["MAIL_SERVER"] = config["flask_mail"]["MAIL_SERVER"]
app.config["MAIL_PORT"] = int(config["flask_mail"]["MAIL_PORT"])
app.config["MAIL_USERNAME"] = config["flask_mail"]["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = config["flask_mail"]["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = config.getboolean("flask_mail", "MAIL_USE_TLS")

mail = Mail(app)

DEFAULT_PIC = "default.jpg"

BP = Blueprint(
    "register", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/", methods=["GET", "POST"])
def register():
    '''Register a new user. Takes input from the RegistrationForm and checks the information for duplicates then adds the user to the database.'''
    form = RegistrationForm()

    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        age = form.age.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        password_confirm = form.password_confirm.data
        picture = DEFAULT_PIC
        print(form.surename.data, type(form.surename.data))
        if form.surename.data is not "":
            return redirect(url_for("index.index"))

        if password != password_confirm:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("register.register"))

        with UsersDB() as db:
            email_cypher, email_hashed = encrypt_email(email)
            
            usernameCheck = db.check_user(username)
            if usernameCheck[next(iter(usernameCheck))]:
                flash(
                    "Username already exists. Please choose a different username.",
                    "error",
                )
                return redirect(url_for("register.register"))

            emailCheck = db.check_email(email_hashed)
            if emailCheck[next(iter(emailCheck))]:
                flash("The provided Email is already connected to an account.", "error")
                return redirect(url_for("register.register"))

            else:
                db.add_new_user(username, generate_password_hash(password), firstName, lastName, email_cypher, age, picture, email_hashed)
                token = app.secret_key
                db.store_token(email_hashed, token)
                send_email(email, token)
                return render_template("verify.html")

    return render_template("register.html", form=form)



def send_email(email: str, token: str) -> None:
    '''Send an email to the user with a link to verify their account.'''
    msg = Message('Account Verification', sender="noreply@lillegaard.com", recipients=[email])

    verify_url = url_for("register.verify_account", token=token, _external=True)
    msg.body = f'Click the following link to verify your account: {verify_url}'
    msg.html = render_template('confirm_email.html', verify_url=verify_url)
    mail.send(msg)


@BP.route("/verify/<token>")
def verify_account(token):
    '''Verify the user's account.'''
    with UsersDB() as db:
        result = db.get_email_by_token(token)
        if result:
            email = result["Email"]
            # Perform account verification SQL query here
            db.verify_user(email)
            db.delete_token(email)
            flash("User successfully verified.", "success") 
            return redirect(url_for("auth.login"))
        else:
            return "Invalid or expired token"
