from app.app import application
from app.user import User
from app.config import config
from flask_login import LoginManager
from app.auth import auth_bp
from app.register import register_bp
from app.index import index_bp
from app.map import map_bp
from app.data import data_bp
from flask_login import current_user

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id) -> User:
    user = User.user_setup("id", user_id)
    if user:
        return user
    return None

application.register_blueprint(register_bp)
application.register_blueprint(auth_bp)
application.register_blueprint(index_bp)
application.register_blueprint(map_bp)
application.register_blueprint(data_bp, url_prefix="/data")
