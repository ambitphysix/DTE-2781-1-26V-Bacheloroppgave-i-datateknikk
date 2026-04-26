from flask import Blueprint, render_template
from flask_login import login_required


BP = Blueprint(
    "map", __name__, static_folder="static", template_folder="templates"
)


@BP.route("/map")
@login_required
def map():
    return render_template("map.html")