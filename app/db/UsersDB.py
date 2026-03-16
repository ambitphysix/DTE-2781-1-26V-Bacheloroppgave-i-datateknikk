from app.db.turist1_db import myDB


class UsersDB(myDB):
    def __init__(self):
        super().__init__()
        pass


    ##############################  USERS  ##############################

    def add_new_user(
        self,
        username: str,
        password: str,
        firstname: str,
        lastname: str,
        email: str,
        age: int,
        Picture: str,
        HashedEmail: str
    ) -> None:

        """Adds a new user to the database."""
        sql_query = """
                    INSERT INTO 
                        User (
                            UserName,
                            FirstName,
                            LastName,
                            Email,
                            Age,
                            Picture,
                            PasswordHash,
                            HashedEmail,
                            CreateTime
                        ) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, NOW());
        """

        self.query(sql_query, username, firstname, lastname, email, age,
                   Picture, password, HashedEmail)
        

    def check_user(self, username: str) -> bool:
        """Checks if user exists."""
        sql_query = "SELECT EXISTS(SELECT 1 FROM User WHERE UserName = %s)"
        self.query(sql_query, username)
        return self.cursor.fetchone()

    def check_email(self, email: str) -> bool:
        """Checks if email adress exists in database."""
        sql_query = "SELECT EXISTS(SELECT 1 FROM User WHERE HashedEmail = %s)"
        self.query(sql_query, email)
        return self.cursor.fetchone()

    def get_all_users_order_username_asc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.UserName ASC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_username_desc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.UserName DESC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_name_asc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.LastName ASC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_name_desc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.LastName DESC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_reason_asc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    WHERE u.Flagged = 1
                    ORDER BY fu.Reason ASC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_reason_desc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    WHERE u.Flagged = 1
                    ORDER BY fu.Reason DESC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_who_asc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    WHERE u.Flagged = 1
                    ORDER BY fu.WhoFlagged ASC
                    LIMIT %s OFFSET %s;
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_who_desc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    WHERE u.Flagged = 1
                    ORDER BY fu.WhoFlagged DESC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_role_asc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.RoleId ASC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_all_users_order_role_desc(self, per_page: int, page: int) -> dict:
        """Returns all users and information about flag status."""
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    ORDER BY u.RoleId DESC
                    LIMIT %s OFFSET %s
                    """
        self.query(sql_query, per_page, page)
        return self.cursor.fetchall()

    def get_email(self, userid):
        """Gets the email adress of a user by user id."""
        sql_query = "SELECT Email FROM User WHERE UserId = %s"
        self.query(sql_query, userid)
        return self.cursor.fetchone()

    def get_user(self, username: str):
        """Gets all columns for a specific user by username."""
        sql_query = "SELECT * FROM User WHERE UserName = %s"
        self.query(sql_query, username)
        return self.cursor.fetchone()

    def get_user_by_id(self, userId):
        """Gets all columns for a specific user by user id."""
        sql_query = "SELECT * FROM User WHERE UserId = %s"
        self.query(sql_query, userId)
        return self.cursor.fetchone()

    def update_newsletter(self, userId, newsletter):
        """Updates the newsletter status of a user."""
        sql_query = "UPDATE User SET Newsletter = %s WHERE UserId = %s"
        self.query(sql_query, newsletter, userId)
    
    def verify_user(self, hash_email: str):
        """Updates verified status of user with email adress \"email\"."""
        sql_query = "UPDATE User SET Verified = 1 WHERE HashedEmail = %s"
        self.query(sql_query, hash_email)

    def update_points(self, user_id: int, points_increment: int):
        """Changes the user's point total by the given amount."""
        sql_query = "UPDATE User SET Points = Points + %s WHERE UserId = %s"
        self.query(sql_query, points_increment, user_id)

    ############################## Friends  ##############################

    def search_usernames(self, username: str, limit=10) -> dict:
        """Search for usernames in the database."""
        sql_query = """
                    SELECT UserId, Username, Picture
                    FROM User
                    WHERE UserName LIKE %s LIMIT %s;
                    """
        self.query(sql_query, "%" + username + "%", limit)
        results = self.cursor.fetchall()
        return results

    def get_friend_requests(self, user_id):
        """Get all friend requests for a user."""
        sql_query = """
                    SELECT u.UserId, u.UserName, u.Picture
                    FROM FriendRequest AS f
                    JOIN User AS u ON f.UserFromId = u.UserId
                    WHERE f.UserToId = %s;
                    """
        self.query(sql_query, user_id)
        return self.cursor.fetchall()

    def get_friend_requests_count(self, user_id):
        """Get the number of friend requests for a user."""
        sql_query = """
                    SELECT COUNT(*) AS request_count
                    FROM FriendRequest
                    WHERE UserToId = %s;
                    """
        self.query(sql_query, user_id)
        result = self.cursor.fetchone()
        if result:
            return result["request_count"]
        else:
            return 0

    def get_friends(self, user_id):
        """Get all friends for a user."""
        sql_query = """
                    SELECT u.UserId, u.UserName, u.Picture, f.FriendTime, u.Points
                    FROM FriendConnection AS f
                    JOIN User AS u ON (f.UserBId = u.UserId AND f.UserAId = %s) OR (f.UserAId = u.UserId AND f.UserBId = %s)
                    """
        self.query(sql_query, user_id, user_id)
        return self.cursor.fetchall()

    def send_friend_request(self, user_from_id, user_to_id):
        """Inserts a new friend request only if the users are not already friends, and there
        are no pending friend requests.
        A user can not send a request to herself.

        Returns True if the request is inserted.
        Returns False if the users are already friends or pending request.
        """
        if user_to_id == user_from_id:
            return False

        sql_query = """
        SELECT COUNT(*) AS friend_count
        FROM FriendConnection
        WHERE (UserAId = %(user_from_id)s AND UserBId = %(user_to_id)s)
           OR (UserAId = %(user_to_id)s AND UserBId = %(user_from_id)s);
        """
        self.query(sql_query, user_from_id=user_from_id, user_to_id=user_to_id)
        already_friends = self.cursor.fetchone()["friend_count"] > 0

        sql_query = """
        SELECT COUNT(*) AS request_count
        FROM FriendRequest
        WHERE (UserFromId = %(user_from_id)s AND UserToId = %(user_to_id)s)
           OR (UserFromId = %(user_to_id)s AND UserToId = %(user_from_id)s);
        """
        self.query(sql_query, user_from_id=user_from_id, user_to_id=user_to_id)
        pending_request = self.cursor.fetchone()["request_count"] > 0

        if already_friends or pending_request:
            return False

        sql_query = """
        INSERT INTO FriendRequest (UserFromId, UserToId)
        VALUES (%s, %s);
        """
        self.query(sql_query, user_from_id, user_to_id)
        return True

    def remove_friend_request(self, user_from_id, user_to_id):
        """Remove the friend request. Does not add a new friend connection"""
        sql_query = """
                DELETE FROM FriendRequest
                WHERE UserFromId = %s
                AND UserToId = %s;
                """
        self.query(sql_query, user_from_id, user_to_id)
        return True

    def accept_friend_request(self, user_from_id, user_to_id):
        """Accept the friend request only if it exists. Adds a new friend connection
        between the users.

        Returns True if successful.
        Returns False if the request does not exist.
        """

        # Check if the request exists
        sql_query = """
        SELECT COUNT(*) AS request_count
        FROM FriendRequest
        WHERE UserFromId = %s
        AND UserToId = %s;
        """
        self.query(sql_query, user_from_id, user_to_id)
        if self.cursor.fetchone()["request_count"] == 0:
            return False

        # add a friend connection
        sql_query = """
        INSERT INTO FriendConnection (UserAId, UserBId)
        VALUES (%s, %s);
        """
        self.query(sql_query, user_from_id, user_to_id)

        # remove the friend request
        self.remove_friend_request(user_from_id, user_to_id)

        return True

    ############################## TOKENS  ##############################

    def store_token(self, email, token):
        sql_query = "INSERT INTO Token (Email, Token) VALUES (%s, %s)"
        self.query(sql_query, email, token)

    def get_email_by_token(self, token):
        sql_query = "SELECT Email FROM Token WHERE Token = %s"
        self.query(sql_query, token)
        return self.cursor.fetchone()

    def delete_token(self, email):
        self.query("DELETE FROM Token WHERE Email = %s", email)

        ############################## ADMIN  ##############################

    def admin_rights(self, value, userId):
        sql_query = "UPDATE User SET RoleId = %s WHERE UserId = %s"
        self.query(sql_query, value, userId)

    def cleanup_db(self):
        sql_query1 = """
                    DELETE FROM Token 
                    WHERE CreateTime < NOW() - INTERVAL 3 HOUR
        """
        self.query(sql_query1)
        sql_query2 = """
                    DELETE FROM User
                    WHERE CreateTime < NOW() - INTERVAL 3 HOUR AND Verified = 0
        """
        self.query(sql_query2)

    def cleanup_flagged(self):
        sql_query = """
                    DELETE FROM User 
                    WHERE UserId IN (
                        SELECT UserId 
                        FROM FlaggedUser 
                        WHERE FlagTime < NOW() - INTERVAL 30 DAY
                    )
        """
        self.query(sql_query)

    def flag_user(self, value, userId):
        sql_query = "UPDATE User SET Flagged = %s WHERE UserId = %s"
        self.query(sql_query, value, userId)

    def flag_user_table_add(self, UserId, UserName, Email, Who, Reason):
        sql_query = """
                    INSERT INTO FlaggedUser 
                        (
                        UserId,
                        UserName,
                        Email,
                        Reason,
                        WhoFlagged,
                        FlagTime
                        )
                    VALUES (%s, %s, %s, %s, %s, NOW())
        """
        self.query(sql_query, UserId, UserName, Email, Who, Reason)

    def flag_user_table_remove(self, UserId):
        self.query("DELETE FROM FlaggedUser WHERE UserId = %s", UserId)

    def get_total_users_count(self):
        self.query("SELECT COUNT(*) AS total FROM User")
        return self.cursor.fetchone()["total"]
    
    def search_users(self, username: str, limit=30):
        sql_query = """
                    SELECT u.*, fu.Reason, fu.WhoFlagged
                    FROM User AS u
                    LEFT JOIN FlaggedUser AS fu ON u.UserId = fu.UserId
                    WHERE u.UserName LIKE %s LIMIT %s;
                    """
        self.query(sql_query, "%" + username + "%", limit)
        results = self.cursor.fetchall()
        return results
