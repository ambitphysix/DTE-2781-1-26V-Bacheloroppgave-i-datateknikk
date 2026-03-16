from app.db.turist1_db import myDB


class StatisticsDB(myDB):
    def __init__(self):
        super().__init__()
        pass

    ############################## ATTRACTIONS  ##############################

    def get_attraction_statistics(self):
        query = """
                SELECT
                    A.AttractionId,
                    A.AttractionName,
                    COUNT(V.VisitId) AS VisitCount
                FROM
                    Attraction A
                LEFT JOIN
                    AttractionVisit V ON A.AttractionId = V.AttractionId
                GROUP BY
                    A.AttractionId, A.AttractionName
                ORDER BY
                    VisitCount DESC
                """
        self.query(query)
        return self.cursor.fetchall()
    ############################## ACHIEVEMENTS  ##############################

    def get_achievement_statistics(self):
        query = """
                SELECT 
                    A.AchievementId,
                    A.AchievementName,
                    A.Description,
                    COUNT(AC.UserId) AS AchievedCount
                FROM 
                    Achievement A
                LEFT JOIN 
                    AchievementConnection AC ON A.AchievementId = AC.AchievementId
                GROUP BY 
                    A.AchievementId, A.AchievementName, A.Description
                ORDER BY
                AchievedCount DESC
                """
        self.query(query)
        return self.cursor.fetchall()
    
    ############################## USERS  ##############################
    
    
    #def get_all_users_statistics(self): #Gets ALL users
    #    query = """
    #            SELECT 
    #                U.UserId,
    #                U.UserName,
    #                COUNT(DISTINCT CASE WHEN FC.UserAId = U.UserId THEN FC.UserBId ELSE FC.UserAId END) AS NumFriends,
    #                COUNT(DISTINCT AV.AttractionId) AS NumAttractionVisits,
    #                COUNT(DISTINCT AC.AchievementId) AS NumAchievementsUnlocked,
    #                U.Points AS TotalAchievementPoints
    #            FROM 
    #                User U
    #            LEFT JOIN 
    #                FriendConnection FC ON U.UserId = FC.UserAId OR U.UserId = FC.UserBId
    #            LEFT JOIN 
    #                AttractionVisit AV ON U.UserId = AV.UserId
    #            LEFT JOIN 
    #                AchievementConnection AC ON U.UserId = AC.UserId
    #            GROUP BY 
    #                U.UserId, U.UserName
#
    #            """
    #    self.query(query)
    #    return self.cursor.fetchall()
    
    def get_active_users_statistics(self): #Gets only users with atleast one attractionvisit
        query = """
                SELECT 
                    U.UserId,
                    U.UserName,
                    COUNT(DISTINCT CASE WHEN FC.UserAId = U.UserId THEN FC.UserBId ELSE FC.UserAId END) AS NumFriends,
                    COUNT(DISTINCT AV.AttractionId) AS NumAttractionVisits,
                    COUNT(DISTINCT AC.AchievementId) AS NumAchievementsUnlocked,
                    U.Points AS TotalAchievementPoints
                FROM 
                    User U
                LEFT JOIN 
                    FriendConnection FC ON U.UserId = FC.UserAId OR U.UserId = FC.UserBId
                INNER JOIN 
                    AttractionVisit AV ON U.UserId = AV.UserId
                LEFT JOIN 
                    AchievementConnection AC ON U.UserId = AC.UserId
                GROUP BY 
                    U.UserId, U.UserName

                """
        self.query(query)
        return self.cursor.fetchall()
