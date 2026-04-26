from app.db import UsersDB
from werkzeug.security import check_password_hash
from flask_login import login_user, UserMixin


class User(UserMixin):
    def __init__(self, UserId, UserName, PasswordHash):
        self.UserId = UserId
        self.UserName = UserName
        self.PasswordHash = PasswordHash

    def user_setup(choice: str, value):
        with UsersDB() as db:
            if choice == "username":
                result = db.get_user(value)
            elif choice == "id":
                result = db.get_user_by_id(value)
            else:
                return False
            if result:
                return User(UserId=result['UserID'], UserName=result['UserName'], PasswordHash=result['PasswordHash'])
            return False

    def login(username, password):
        user = User.user_setup('username', username)
        if not user or not check_password_hash(user.PasswordHash, password):
            return False
        else:
            login_user(user, remember=True)
            return 'success'
        return False

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        return self.UserId
