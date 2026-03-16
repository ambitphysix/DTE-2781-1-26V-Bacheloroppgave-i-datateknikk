from typing import Any


class Attraction_statistics:
    def __init__(self, AttractionId, AttractionName, VisitCount):
        self.AttractionId = AttractionId
        self.AttractionName = AttractionName
        self.VisitCount = VisitCount


class Achievement_statistics:
    def __init__(self, AchievementId, AchievementName, Description, AchievedCount):
        self.AchievementId = AchievementId
        self.AchievementName = AchievementName
        self.Description = Description
        self.AchievedCount = AchievedCount
        

class User_statistics:
    def __init__(self, UserId, UserName, NumFriends, NumAttractionVisits, NumAchievementsUnlocked, TotalAchievementPoints):
        self.UserId = UserId
        self.UserName = UserName
        self.NumFriends = NumFriends
        self.NumAttractionVisits = NumAttractionVisits
        self.NumAchievementsUnlocked = NumAchievementsUnlocked
        self.TotalAchievementPoints = TotalAchievementPoints
