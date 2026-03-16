from flask import request, render_template, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_required
from app.db.AttractionsDB import AttractionsDB
from app.db.UsersDB import UsersDB
from app.achievements.achievements import search_for_new_achievements
from app.Classes import Attraction, AttractionTypes


BP = Blueprint(
    "attractions", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/", methods=["GET", "POST"])
@login_required
def attractions():
    attractionType = request.args.get("attractiontype")
    user_id = current_user.get_id()
    filterType = request.args.get("filtertype")
    sort_by = request.args.get("sortby")
    page = request.args.get(
        "page", 1, type=int
    )  # Get the page number from the request, default to 1
    per_page = 10  # Number of items per page
    offset = (page - 1) * per_page  # Calculate the offset for the query
    attractions = []
    lower_age = request.args.get("lower_age")
    upper_age = request.args.get("upper_age")

    if not lower_age:
        lower_age = "0"

    if not upper_age:
        upper_age = "99"

    with AttractionsDB() as db:
        attractionTypes = [
            AttractionTypes(x["TypeId"], x["TypeName"]) for x in db.getAttractionTypes()
        ]
        total_attraction = db.get_total_attraction_count()
        hide_visited = current_user.hide_visited_attractions

        if attractionType == "all":
            if filterType == "user_age" and current_user.Age:
                result = db.getAttractionsFilteredByAge(
                    user_id, current_user.Age, per_page, offset
                )
            elif sort_by == "Popularity":
                result = db.get_attractions_sorted(user_id, per_page, offset)
            elif filterType == "agefilter":
                result = db.get_attractions_filtered_by_age(
                    user_id, lower_age, upper_age, per_page, offset
                )
            else:
                result = db.getAttractions(per_page, offset, user_id)
        else:
            if filterType == "user_age" and current_user.Age:
                result = db.getAttractionsByTypeFilteredByAge(
                    attractionType, user_id, current_user.Age, per_page, offset
                )
            elif sort_by == "Popularity":
                result = db.get_attractions_by_type_and_sorted(
                    attractionType, user_id, per_page, offset
                )
            else:
                result = db.getAttractionsByType(
                    attractionType, per_page, offset, user_id
                )

        if result is not None:
            attractions = [Attraction(**x) for x in result]

    return render_template(
        "attractions.html",
        attractionTypes=attractionTypes,
        attractions=attractions,
        total_attraction=total_attraction,
        page=page,
        per_page=per_page,
        hide_visited=hide_visited,
    )


@BP.route("/visit", methods=["POST"])
@login_required
def visit():
    attraction_id = request.form.get("attractionId")
    current_type = request.form.get("currentType")
    user_id = current_user.UserId

    with AttractionsDB() as db:
        db.update_visited_attractions(user_id, attraction_id)
    with UsersDB() as db:
        db.update_points(user_id, current_user.POINTS_AWARDED_PER_ACHIEVEMENT)
    flash("Attraction visited!")

    search_for_new_achievements(current_user.UserId)

    return redirect(url_for("attractions.attractions", attractiontype=current_type))


@BP.route("/page/<int:attraction_id>", methods=["GET"])
@login_required
def page(attraction_id):
    with AttractionsDB() as db:
        attraction = db.getAttractionById(attraction_id)

    return render_template("attraction_page.html", attraction=attraction)
