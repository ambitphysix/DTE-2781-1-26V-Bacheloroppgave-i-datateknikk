from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import current_user
from app.db.turist1_db import myDB
from app.db.UsersDB import UsersDB
from app.db.StatisticsDB import StatisticsDB
from app.UserForm import GetUser, SearchUsernames
from app.user import User_Extended
from functools import wraps
from app.admin.report_classes import Attraction_statistics, Achievement_statistics, User_statistics

BP = Blueprint(
    "admin", __name__, static_folder="app/static", template_folder="app/templates"
)

# Decorator for admin required pages
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.RoleId != 2:
            return redirect(url_for("index.index"))
        return func(*args, **kwargs)

    return decorated_function


@BP.route("/", methods=["GET", "POST"])
@admin_required
def admin():
    moderator_choice = request.args.get(
        "moderator_choice"
    )  # Get the admin choice from the request
    order = request.args.get(
        "order", 1, type=int
    )  # Get the order from the request, default to ascending username
    page = request.args.get(
        "page", 1, type=int
    )  # Get the page number from the request, default to 1
    per_page = 30  # Number of items per page
    offset = (page - 1) * per_page  # Calculate the offset for the query
    form = GetUser()
    search_form = SearchUsernames()
    if search_form.validate_on_submit(): 
        search_term = search_form.search_term.data
    else:
        search_term = ""

    if not moderator_choice:
        return render_template("admin.html")
    elif moderator_choice == "Reports":
        return render_template("reports.html")
    else:
        with UsersDB() as db:
            if len(search_term) > 2:
                result = db.search_users(search_term)
                for x in result:
                    print(x)
                Users = [User_Extended(**x) for x in result] 
                total_users = len(Users)
            else:       
                # Get the users based on the admin choice
                order_by = {
                    1: db.get_all_users_order_username_asc,
                    2: db.get_all_users_order_username_desc,
                    3: db.get_all_users_order_name_asc,
                    4: db.get_all_users_order_name_desc,
                    5: db.get_all_users_order_reason_asc,
                    6: db.get_all_users_order_reason_desc,
                    7: db.get_all_users_order_who_asc,
                    8: db.get_all_users_order_who_desc,
                    9: db.get_all_users_order_role_asc,
                    10: db.get_all_users_order_role_desc,
                }
                if order in order_by:
                    result = order_by[order](per_page, offset)
                Users = [User_Extended(**x) for x in result]
                total_users = db.get_total_users_count()
        return render_template(
            "admin.html",
            current_user=current_user,
            Users=Users,
            form=form,
            moderator_choice=moderator_choice,
            page=page,
            per_page=per_page,
            total_users=total_users,
            order=order,
            search_form=search_form,
        )


@BP.route("/flagged", methods=["GET", "POST"])
@admin_required
def flagged():
    """This function is used to flag or unflag a user. It is only accessible to users with admin rights."""
    form = GetUser()
    search_form = SearchUsernames()
    if search_form.validate_on_submit():
        search_term = search_form.search_term.data
    if form.validate_on_submit():
        uid = form.uid.data
        value = int(form.value.data)
        with UsersDB() as db:
            db.flag_user(value, uid)

            if value == 0:
                flash("User successfully unflagged.", "success")
                db.flag_user_table_remove(uid)
            else:
                db.flag_user_table_add(
                    uid,
                    form.username.data,
                    form.email.data,
                    form.reason.data,
                    form.who.data,
                )
                flash("User successfully flagged.", "success")
        return redirect(
            url_for(
                "admin.admin",
                moderator_choice="Flag",
                page=form.page.data,
                order=form.order.data,
            )
        )
    return render_template("admin.html")


@BP.route("/rights", methods=["GET", "POST"])
@admin_required
def rights():
    """This function is used to add or remove admin rights from a user. It is only accessible to users with admin rights."""
    form = GetUser()
    if form.validate_on_submit():
        uid = form.uid.data
        value = int(form.value.data)
        with UsersDB() as db:
            db.admin_rights(value, uid)
            if value == 2:
                flash("Added admim rights.", "success")
            else:
                flash("Removed admin rights", "success")
        return redirect(
            url_for(
                "admin.admin",
                moderator_choice="Moderator",
                page=form.page.data,
                order=form.order.data,
            )
        )
    else:
        print("Form not validated")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template("admin.html")


@BP.route("/reports", methods=["GET", "POST"])
@admin_required
def reports():
    report_choice = request.args.get("report_choice")
    if not report_choice:
        return render_template("reports.html")

    elif report_choice == "Attractions":
        with StatisticsDB() as db:
            result = db.get_attraction_statistics()
            statistics = [Attraction_statistics(**x) for x in result]
        return render_template("reports.html", report_choice=report_choice, statistics=statistics)

    elif report_choice == "Achievement":
        with StatisticsDB() as db:
            result = db.get_achievement_statistics()
            statistics = [Achievement_statistics(**x) for x in result]
        return render_template("reports.html", report_choice=report_choice, statistics=statistics)
    elif report_choice == "User":
        with StatisticsDB() as db:
            result = db.get_active_users_statistics()
            statistics = [User_statistics(**x) for x in result]
        return render_template("reports.html", report_choice=report_choice, statistics=statistics)
    

    else:
        return render_template("reports.html")
    
    
    
@BP.route("/csv", methods=["GET"])
def download_csv():
    download_choice = request.args.get("download")
    with StatisticsDB() as db:
        if download_choice == "User":
            result = db.get_active_users_statistics()
        elif download_choice == "Achievement":
            result = db.get_achievement_statistics()
        elif download_choice == "Attraction":
            result = db.get_attraction_statistics()
            
    csv_content = get_csv_content_from_query(result)
     # Set up the response
    response = make_response(csv_content)
    response.headers['Content-Disposition'] = f'attachment; filename={download_choice}Statistics.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response



def get_csv_content_from_query(data):

    # Extract the keys (column names) from the first dictionary
    keys = data[0].keys() if data else []

    # Create CSV 
    csv_content = ','.join(keys) + '\n'
    csv_content += '\n'.join([','.join(map(str, row.values())) for row in data])
    
    return csv_content