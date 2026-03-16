from flask import Blueprint, render_template
from flask_login import current_user


BP = Blueprint(
    "index", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/")
def index():
    if current_user.is_authenticated:
        user_info = {"username": current_user.UserName, "email": current_user.Email}
        return render_template("index.html", user_info=user_info)
    else:
        return render_template("index.html")
