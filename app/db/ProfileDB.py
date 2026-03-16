from app.db.turist1_db import myDB


class ProfileDB(myDB):
    def __init__(self):
        super().__init__()
        pass

    ############################## PROFILE  ##############################

    def updateProfile(self, values: tuple):
        """Updates a user profile with values in tuple \"values\"."""
        sql_query = """
                    UPDATE
                        User 
                    SET 
                        FirstName = %s,
                        LastName = %s,
                        Picture = %s
                    WHERE UserId = %s
        
        """
        self.query(sql_query, *values)

    def updateLastVisit(self, userId):
        """Updates a user with timestamp NOW() by userId."""
        sql_query = "UPDATE User SET LastVisit = NOW() WHERE UserId = %s"
        self.query(sql_query, userId)

    def toggle_hide_visited_attractions(self, user_id, hide_visited):
        """Updates the user's preference to hide or show visited attractions."""
        sql_query = "UPDATE User SET HideVisitedAttractions = %s WHERE UserId = %s"
        self.query(sql_query, hide_visited, user_id)
