class AttractionTypes:
    def __init__(self, typeId, attractionType):
        self.typeId = typeId
        self.attractionType = attractionType


class Attraction:
    def __init__(
        self,
        AttractionId,
        TypeId,
        TypeName,
        AttractionName,
        Description,
        Picture,
        AgeFrom,
        AgeTo,
        Points,
        Address,
        Location,
        Visited,
        Popularity=None,
    ):
        self.AttractionId = AttractionId
        self.TypeId = TypeId
        self.TypeName = TypeName
        self.AttractionName = AttractionName
        self.Description = Description
        self.Picture = Picture
        self.AgeFrom = AgeFrom
        self.AgeTo = AgeTo
        self.Points = Points
        self.Address = Address
        self.Location = Location
        self.Visited = Visited
        self.Popularity = Popularity


class AttractionVisit:
    def __init__(self, attraction_id, attraction_name, time_difference):
        self.attraction_id = attraction_id
        self.attraction_name = attraction_name
        self.time_difference = time_difference
        self.time_difference_as_string = self.get_time_string(time_difference)

    @staticmethod
    def get_time_string(time_difference):
        days = time_difference.days
        hours = time_difference.seconds // 3600
        minutes = time_difference.seconds // 60

        if days > 0:
            return f"{days} day{'s' if days > 1 else ''} ago"
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        if minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        return "Just now"
