from app.db.turist1_db import myDB
from app.db.UsersDB import UsersDB
from app.db.ProfileDB import ProfileDB
from werkzeug.security import check_password_hash
from flask_login import login_user, UserMixin


class User(UserMixin):
    POINTS_AWARDED_PER_VISIT = 10
    POINTS_AWARDED_PER_ACHIEVEMENT = 25
    POINTS_REQUIRED_PER_LEVEL = 100

    # construct / attributes

    def __init__(self, UserId, RoleId, UserName, FirstName, LastName, Email, Age, Picture, PasswordHash, CreateTime,
                 Verified, LastVisit, Flagged, Newsletter, hide_visited_attractions, points, HashedEmail):

        self.UserId = UserId
        self.RoleId = RoleId
        self.UserName = UserName
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Age = Age
        self.Picture = Picture
        self.PasswordHash = PasswordHash
        self.CreateTime = CreateTime
        self.Verified = Verified
        self.LastVisit = LastVisit
        self.Flagged = Flagged
        self.Newsletter = Newsletter
        self.hide_visited_attractions = hide_visited_attractions

        self.points = 0
        self.level = 0
        self.level_fraction = 0.0
        self.update_points(points) 
        self.HashedEmail = HashedEmail

    def user_setup(choice: str, value):
        with UsersDB() as db:
            if choice == "username":
                result = db.get_user(value)
            elif choice == "id":
                result = db.get_user_by_id(value)
            else:
                return False
            if result:

                user = User(UserId=result['UserId'], 
                            RoleId=result['RoleId'], 
                            UserName=result['UserName'], 
                            FirstName=result['FirstName'], 
                            LastName=result['LastName'], 
                            Email=result['Email'], 
                            Age=result['Age'], 
                            Picture=result['Picture'], 
                            PasswordHash=result['PasswordHash'], 
                            CreateTime=result['CreateTime'], 
                            Verified=result['Verified'],
                            LastVisit=result['LastVisit'],
                            Flagged=result['Flagged'],
                            Newsletter=result['Newsletter'],
                            hide_visited_attractions=result['HideVisitedAttractions'],
                            points=result['Points'],
                            HashedEmail=result['HashedEmail'])
                return user
            return False

    def login(username, password):
        user = User.user_setup('username', username)
        if not user or not check_password_hash(user.PasswordHash, password):
            return False

        if user.Flagged:
            return 'flagged'

        if user.Verified: 
            with ProfileDB() as db:
                db.updateLastVisit(user.UserId) 
            login_user(user, remember=True)
            return 'success'
        return False

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        return self.UserId

    @staticmethod
    def convert_points_to_level(points):
        """Calculate which level the user has. Each level requires 100 points"""
        return points // User.POINTS_REQUIRED_PER_LEVEL

    @staticmethod
    def fraction_of_level_completed(points):
        """Calculate how large fraction of the current level is completed.

        Returns a float between 0 (0% progress of the current level) and 1 (100% progress in the
        current level).
        """
        return (
            points % User.POINTS_REQUIRED_PER_LEVEL
        ) / User.POINTS_REQUIRED_PER_LEVEL

    def set_level_fields(self, points):
        """Calculates and sets the fields relevant for points and levels."""
        self.points = points
        self.level = self.convert_points_to_level(self.points)
        self.level_fraction = self.fraction_of_level_completed(self.points)

    def update_points(self, points_increment):
        """Increases the amount of points by the given amount."""
        if self.points is None:
            self.points = 0
        if points_increment is None:
            points_increment = 0
        self.set_level_fields(self.points + points_increment)


class User_Extended(User):
    def __init__(self, UserId, RoleId, UserName, FirstName, LastName, Email, Age, Picture, PasswordHash, CreateTime, Verified, LastVisit, Flagged, Newsletter, HideVisitedAttractions, Reason, WhoFlagged, Points, HashedEmail):
        super().__init__(UserId, RoleId, UserName, FirstName, LastName, Email, Age, Picture, PasswordHash, CreateTime, Verified, LastVisit, Flagged, Newsletter, HideVisitedAttractions, Points, HashedEmail)

        self.Reason = Reason
        self.WhoFlagged = WhoFlagged
