from flask import Blueprint, render_template


BP = Blueprint(
    "index", __name__, static_folder="static", template_folder="templates"
)


@BP.route("/")
def index():
    return render_template("index.html")