from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask import send_from_directory
from flask_login import current_user
from app.Classes import AttractionVisit
from flask_login import login_required
from app.db.turist1_db import myDB
from app.db.UsersDB import UsersDB
from app.db.AttractionsDB import AttractionsDB
from app.db.ProfileDB import ProfileDB
from app.UserForm import ProfileEditForm, GetNewsletter
from config import config
from app.profile.utils import allowed_file
import os

BP = Blueprint(
    "profile", __name__, static_folder="app/static", template_folder="app/templates"
)


@BP.route("/", methods=["GET", "POST"])
@login_required
def profile():
    news_form = GetNewsletter()
    with AttractionsDB() as db:
        result = db.get_recent_attraction_visits_by_user(current_user.UserId)
        attraction_visits = [AttractionVisit(*row.values()) for row in result]
        user_achievements = db.get_achievements_obtained_by_user(current_user.UserId)
    return render_template(
        "profile.html",
        User=current_user,
        news_form=news_form,
        attraction_visits=attraction_visits,
        user_achievements=user_achievements,
    )


@BP.route("/toggle_hide_visited_attractions", methods=["POST"])
@login_required
def toggle_hide_visited_attractions():
    # Henter nåværende verdi av hide_visited_attractions for å veksle den
    new_preference = not current_user.hide_visited_attractions
    with ProfileDB() as db:
        db.toggle_hide_visited_attractions(current_user.UserId, new_preference)
    flash("Your preference has been updated")
    return redirect(url_for("profile.profile"))


@BP.route("/newsletter", methods=["POST"])
@login_required
def newsletter():
    news_form = GetNewsletter()
    if news_form.validate_on_submit():
        with UsersDB() as db:
            db.update_newsletter(current_user.UserId, int(news_form.newsletter.data))
            return redirect(url_for("profile.profile"))
    return render_template("profile.html", news_form=news_form)


@BP.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    print("Handling edit_profile route. Current URL:", request.url)
    form = ProfileEditForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        file = form.picture.data
        if file and allowed_file(file.filename):
            hashed_filename = allowed_file(file.filename)
            file.save(
                os.path.join(os.path.dirname(__file__), "../uploads", hashed_filename)
            )
            picture = hashed_filename
        else:
            picture = current_user.Picture
        try:
            with ProfileDB() as db:
                values = (
                    firstname,
                    lastname,
                    picture,
                    current_user.UserId,
                )
                db.updateProfile(values)
                flash("Profile updated successfully", "success")
                return redirect(url_for("profile.profile"))
        except Exception as e:
            flash("An error occurred during updating. Please try again.", "error")
            print("Error during updating profile:", e)
    form.firstname.data = current_user.FirstName
    form.lastname.data = current_user.LastName
    form.picture.data = current_user.Picture
    return render_template("edit_profile.html", form=form)


@login_required
@BP.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(config["upload_folder"]["UPLOAD_FOLDER"], filename)
