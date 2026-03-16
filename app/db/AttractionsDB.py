from app.db.turist1_db import myDB


class AttractionsDB(myDB):
    def __init__(self):
        super().__init__()
        pass

    ############################## ATTRACTIONS  ##############################

    def getAttractionTypes(self):
        self.query("SELECT TypeId, TypeName FROM AttractionType")
        return self.cursor.fetchall()

    def getAttractions(self, page, offset, user_id=None):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location, 
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                LIMIT %s OFFSET %s
                """
        self.query(query, user_id, page, offset)
        return self.cursor.fetchall()

    def getAttractionById(self, attraction_id):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    X(A.Location) AS Latitude,
                    Y(A.Location) AS Longitude
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AT ON A.TypeId = AT.TypeId
                WHERE 
                    A.AttractionId = %s
                """
        self.cursor.execute(query, (attraction_id,))
        return self.cursor.fetchone()

    def getAttractionsByType(self, attractionType, page, offset, user_id=None):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location, 
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                WHERE 
                    AT.TypeName = %s
                LIMIT %s OFFSET %s
        """
        self.query(query, user_id, attractionType, page, offset)
        return self.cursor.fetchall()

    def has_visited(self, user_id, attraction_id):
        sql_query = """
                    SELECT 
                        EXISTS ( 
                            SELECT 1
                            FROM AttractionVisit
                            WHERE UserId = %s AND AttractionId = %s 
                        ) AS visited
        """
        self.query(sql_query, user_id, attraction_id)
        result = self.cursor.fetchone()
        return bool(result["visited"]) if result else False

    def update_visited_attractions(self, user_id, attraction_id):
        if not self.has_visited(user_id, attraction_id):
            sql_query = """
                        INSERT INTO AttractionVisit (UserId, AttractionId)
                        VALUES (%s, %s)
            """
            self.query(sql_query, user_id, attraction_id)
            return True  # Besøket ble loggført
        else:
            return False  # Besøket var allerede loggført, ingen handling utført

    def getAttractionsFilteredByAge(self, user_id, age, page, offset):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location, 
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                WHERE 
                    A.AgeFrom <= %s 
                    AND A.AgeTo >= %s
                LIMIT %s OFFSET %s
            """
        self.query(query, user_id, age, age, page, offset)
        return self.cursor.fetchall()

    def getAttractionsByTypeFilteredByAge(
        self, attractionType, user_id, age, page, offset
    ):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location, 
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                WHERE 
                    AT.TypeName = %s 
                    AND A.AgeFrom <= %s 
                    AND A.AgeTo >= %s
                LIMIT %s OFFSET %s
            """
        self.query(query, user_id, attractionType, age, age, page, offset)
        return self.cursor.fetchall()

    def get_attractions_sorted(self, user_id, page, offset):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location,
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited,
                    AVC.Popularity
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                LEFT JOIN (
                    SELECT 
                        AttractionId,
                        COUNT(*) AS Popularity
                    FROM AttractionVisit
                    GROUP BY AttractionId
                ) AS AVC ON AVC.AttractionID = A.AttractionId
                ORDER BY Popularity DESC
                LIMIT %s OFFSET %s
            """
        self.query(query, user_id, page, offset)
        return self.cursor.fetchall()

    def get_attractions_by_type_and_sorted(self, attractionType, user_id, page, offset):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location,
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited,
                    AVC.Popularity
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                LEFT JOIN (
                    SELECT 
                        AttractionId,
                        COUNT(*) AS Popularity
                    FROM AttractionVisit
                    GROUP BY AttractionId
                ) AS AVC ON AVC.AttractionID = A.AttractionId
                WHERE 
                    AT.TypeName = %s
                ORDER BY Popularity DESC
                LIMIT %s OFFSET %s
            """
        self.query(query, user_id, attractionType, page, offset)
        return self.cursor.fetchall()

    def get_recent_attraction_visits_by_user(self, user_id, max_visits=5):
        query = """
                SELECT
                    A.AttractionId,
                    A.AttractionName,
                    TIMEDIFF(NOW(), AV.VisitTime)
                FROM AttractionVisit AS AV
                INNER JOIN User AS U ON AV.UserId = U.UserId
                INNER JOIN Attraction AS A ON AV.AttractionId = A.AttractionId
                WHERE U.UserId = %s
                ORDER BY AV.VisitTime DESC
                LIMIT %s;
        """
        self.query(query, user_id, max_visits)
        return self.cursor.fetchall()

    def get_total_attraction_count(self):
        """Returns the total number of attractions in the database."""
        self.query("SELECT COUNT(*) AS total FROM Attraction")
        return self.cursor.fetchone()["total"]

    def get_attraction_ids_visited_by_user(self, user_id):
        query = """
                SELECT 
                    A.AttractionId
                FROM AttractionVisit AS AV
                INNER JOIN User AS U ON AV.UserId = U.UserId
                INNER JOIN Attraction AS A ON AV.AttractionId = A.AttractionId
                WHERE U.UserId = %s;
        """
        self.query(query, user_id)
        return self.cursor.fetchall()

    def get_attractions_filtered_by_age(
        self, user_id, lower_age, upper_age, per_page, offset
    ):
        query = """
                SELECT 
                    A.AttractionId, 
                    A.TypeId, 
                    AT.TypeName, 
                    A.AttractionName, 
                    A.Description, 
                    A.Picture, 
                    A.AgeFrom, 
                    A.AgeTo, 
                    A.Points, 
                    A.Address, 
                    A.Location, 
                    EXISTS (
                        SELECT 1 
                        FROM AttractionVisit AS AV
                        WHERE AV.AttractionId = A.AttractionId 
                        AND AV.UserId = %s
                    ) AS Visited
                FROM 
                    Attraction A
                JOIN 
                    AttractionType AS AT ON A.TypeId = AT.TypeId
                WHERE 
                    A.AgeFrom >= %s 
                    AND A.AgeTo <= %s
                LIMIT %s OFFSET %s;
            """
        self.query(query, user_id, lower_age, upper_age, per_page, offset)
        return self.cursor.fetchall()

    ########################### Achievements  ###########################

    def insert_achievement_connection(self, user_id, achievement_id):
        query = """
                INSERT INTO AchievementConnection (UserId, AchievementId)
                VALUES (%s, %s);
        """
        self.query(query, user_id, achievement_id)

    def get_achievements_not_obtained_by_user(self, user_id):
        query = """
                SELECT
                A.AchievementId,
                A.AchieveCode
            FROM Achievement AS A
            LEFT JOIN AchievementConnection AS AC
                ON A.AchievementId = AC.AchievementId
                AND AC.UserId = %s
            WHERE AC.UserId IS NULL;
        """
        self.query(query, user_id)
        return self.cursor.fetchall()

    def get_achievements_obtained_by_user(self, user_id):
        query = """
            SELECT A.AchievementName, A.Description, A.Picture 
            FROM Achievement AS A
            LEFT JOIN AchievementConnection AS AC
            ON A.AchievementId = AC.AchievementId
            WHERE AC.UserId like %s; 
            """

        self.query(query, user_id)
        return self.cursor.fetchall()

    def get_remaining_achievements(self, user_id):
        query = """
            SELECT A.AchievementName, A.Description, A.Picture
            FROM Achievement AS A
            LEFT JOIN AchievementConnection AS AC
            ON A.AchievementId = AC.AchievementId
            AND AC.UserId = %s
            WHERE AC.UserId IS NULL;
            """

        self.query(query, user_id)
        return self.cursor.fetchall()
