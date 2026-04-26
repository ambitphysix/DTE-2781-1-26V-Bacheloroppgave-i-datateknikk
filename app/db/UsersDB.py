from app.db.MySQLDB import mySQLDB


class UsersDB(mySQLDB):
    def __init__(self):
        super().__init__()
        pass

    def add_new_user(
        self,
        username: str,
        password: str,
    ) -> None:

        """Adds a new user to the database."""
        sql_query = """
                    INSERT INTO 
                        User (
                            UserName,
                            PasswordHash
                        ) 
                    VALUES 
                        (%s, %s);
        """

        self.query(sql_query, username,  password)
        

    def check_user(self, username: str) -> bool:
        """Checks if user exists."""
        sql_query = "SELECT EXISTS(SELECT 1 FROM User WHERE UserName = %s)"
        self.query(sql_query, username)
        return self.cursor.fetchone()

    def get_user(self, username: str):
        """Gets all columns for a specific user by username."""
        sql_query = "SELECT * FROM User WHERE UserName = %s"
        self.query(sql_query, username)
        return self.cursor.fetchone()

    def get_user_by_id(self, userId):
        """Gets all columns for a specific user by user id."""
        sql_query = "SELECT * FROM User WHERE UserID = %s"
        self.query(sql_query, userId)
        return self.cursor.fetchone()
