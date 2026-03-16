from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import login_required, current_user
from flask import flash, redirect, url_for
from app.db.UsersDB import UsersDB
from app.db.AttractionsDB import AttractionsDB
from app.UserForm import SearchUsernames
from app.UserForm import GetNewsletter
from app.Classes import AttractionVisit
from app.user import User

BP = Blueprint(
    "friends", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/", methods=["GET"])
@login_required
def friends():
    """Show friends."""
    with UsersDB() as db:
        friend_requests = db.get_friend_requests(current_user.UserId)
        friends = db.get_friends(current_user.UserId)

        # Calculate friend levels and sort
        for f in friends:
            f['Level'] = User.convert_points_to_level(f['Points'])
        friends.sort(key=lambda f: f['Points'], reverse=True)
    return render_template(
        "friends.html", friend_requests=friend_requests, friends=friends
    )


@BP.route("/friend_request", methods=["GET"])
@login_required
def friend_request():
    """Show friend requests and friends."""
    with UsersDB() as db:
        friend_requests = db.get_friend_requests(current_user.UserId)
        friends = db.get_friends(current_user.UserId)
    return render_template(
        "friend_requests.html", friend_requests=friend_requests, friends=friends
    )


@BP.route("/search_friends", methods=["GET", "POST"])
@login_required
def search_usernames():
    """Search for usernames in the database."""
    form = SearchUsernames()
    users_found = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        with UsersDB() as db:
            users_found = db.search_usernames(search_term)
    return render_template("friend_search.html", form=form, users_found=users_found)


@BP.route("/send_friend_request", methods=["POST"])
@login_required
def handle_send_friend_request():
    """Send a friend request to another user."""
    user_from_id = current_user.UserId
    user_to_id = int(request.form["user_to_id"])
    with UsersDB() as db:
        if db.send_friend_request(user_from_id, user_to_id):
            flash("Friend request sent! Your friend will have to accept.")
        else:
            flash("Could not send friend request.", "error")
    return redirect(url_for("friends.search_usernames"))


@BP.route("/accept_friend_request", methods=["POST"])
@login_required
def handle_accept_friend_request():
    """Accept a friend request."""
    user_from_id = request.form["user_from_id"]
    user_to_id = current_user.UserId
    with UsersDB() as db:
        if db.accept_friend_request(user_from_id, user_to_id):
            flash("Friend request accepted!")
        else:
            flash("Could not accept friend request.", "error")
    return redirect(url_for("friends.friend_request"))


@BP.route("/remove_friend_request", methods=["POST"])
@login_required
def handle_remove_friend_request():
    """Remove a friend request."""
    user_from_id = request.form["user_from_id"]
    user_to_id = current_user.UserId
    with UsersDB() as db:
        if db.remove_friend_request(user_from_id, user_to_id):
            flash("Friend request removed.")
        else:
            flash("Could not remove friend request.", "error")
    return redirect(url_for("friends.friend_request"))

@BP.route("/view/<int:user_id>", methods=["GET", "POST"])
@login_required
def view_friend(user_id):
    """View a friend profile."""
    news_form = GetNewsletter()
    with UsersDB() as db:
        friend = db.get_user_by_id(user_id)
    
    with AttractionsDB() as db:
        result = db.get_recent_attraction_visits_by_user(user_id)
        attraction_visits = [AttractionVisit(*row.values()) for row in result]
        friend_achievements = db.get_achievements_obtained_by_user(user_id)
        friend["hide_visited_attractions"] = friend.pop("HideVisitedAttractions", None)
        friend["points"] = friend.pop("Points", None)
    
    if friend:
        return render_template("profile.html", User=User(**friend),news_form=news_form,
        attraction_visits=attraction_visits,
        user_achievements=friend_achievements,)
    else:
        flash("Friend not found.", "error")
        return redirect(url_for("friends.friends"))