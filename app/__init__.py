from app.app import application
from app.user import User
from app.db.turist1_db import myDB
from config import config
from flask_login import LoginManager
from app.admin import admin_bp
from app.profile import profile_bp
from app.attractions import attractions_bp
from app.auth import auth_bp
from app.register import register_bp
from app.index import index_bp
from app.friends import friends_bp
from app.achievements import achievements_bp
from app.db.UsersDB import UsersDB
from flask_login import current_user

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id) -> User:
    user = User.user_setup("id", user_id)
    if user and not user.Flagged:
        return user
    return None


@application.context_processor
def friend_request_counter():
    """Add friend request counter to all templates."""
    if current_user.is_authenticated:
        user_to_id = current_user.UserId
        friend_requests_count = 0
        with UsersDB() as db:
            friend_requests_count = db.get_friend_requests_count(user_to_id)
        return dict(friend_requests_count=friend_requests_count)
    return dict(friend_requests_count=0)

@application.context_processor
def friend_request_list():
    """Add friend request list to all templates."""
    if current_user.is_authenticated:
        friend_requests = []
        with UsersDB() as db:
            friend_requests = db.get_friend_requests(current_user.UserId)
        return dict(friend_requests=friend_requests)
    return dict(friend_requests=[])


application.register_blueprint(admin_bp, url_prefix="/admin")
application.register_blueprint(profile_bp, url_prefix="/profile")
application.register_blueprint(friends_bp, url_prefix="/friends")
application.register_blueprint(attractions_bp, url_prefix="/attractions")
application.register_blueprint(register_bp, url_prefix="/register")
application.register_blueprint(achievements_bp, url_prefix="/achievements")
application.register_blueprint(index_bp, url_prefix="/")
application.register_blueprint(auth_bp)
