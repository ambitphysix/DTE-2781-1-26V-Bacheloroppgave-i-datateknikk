from flask import flash, Blueprint, render_template
from app.db.UsersDB import UsersDB
from app.db.AttractionsDB import AttractionsDB
from flask_login import current_user, login_required

BP = Blueprint(
    "achievements",
    __name__,
    static_folder="app/static",
    template_folder="app/templates",
)


@BP.route("/", methods=["GET", "POST"])
@login_required
def achievements():
    with AttractionsDB() as db:
        achievements_obtained = db.get_achievements_obtained_by_user(
            current_user.UserId
        )
        achievements_not_obtained = db.get_remaining_achievements(current_user.UserId)

    return render_template(
        "achievements.html",
        current_user=current_user,
        achievements_obtained=achievements_obtained,
        achievements_not_obtained=achievements_not_obtained,
    )


def search_for_new_achievements(user_id):
    with AttractionsDB() as db:
        result = db.get_achievements_not_obtained_by_user(user_id)
        possible_achievements = [list(row.values()) for row in result]

        result = db.get_attraction_ids_visited_by_user(user_id)
        visited_attraction_ids = {list(row.values())[0] for row in result}

    # Search for any new achievements the user has achieved
    new_achievement_ids = []
    for achievement_id, achieve_code in possible_achievements:
        # See insert_data_achievements.sql for a description of achieve codes
        achievement_type = achieve_code[:2]
        achievement_details = achieve_code[2:]

        if achievement_type == "at":
            # Achievement requires one or more specific attraction visits

            required_attraction_ids = {
                int(val) for val in achievement_details.split(",")
            }
            if required_attraction_ids.issubset(visited_attraction_ids):
                new_achievement_ids.append(achievement_id)

        elif achievement_type == "po":
            # Achievement requires a minimum number of points

            required_points = int(achievement_details)
            if current_user.points >= required_points:
                new_achievement_ids.append(achievement_id)

        elif achievement_type == "an":
            # Achievement requires a minimum number of visited attractions

            required_visits = int(achievement_details)
            if len(visited_attraction_ids) >= required_visits:
                new_achievement_ids.append(achievement_id)

    # Award the new achievements to the user
    for achievement_id in new_achievement_ids:
        award_achievement_to_user(user_id, achievement_id)


def award_achievement_to_user(user_id, achievement_id):
    with AttractionsDB() as db:
        db.insert_achievement_connection(user_id, achievement_id)
    with UsersDB() as db:
        db.update_points(user_id, current_user.POINTS_AWARDED_PER_ACHIEVEMENT)

    # To-do: Alert the user properly
    flash(f"You have been awarded an achievement!")
