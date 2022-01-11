import mongoengine


class RunningInfo(mongoengine.Document):
    showId = mongoengine.ObjectIdField(default=None)
    sessionId = mongoengine.ObjectIdField(default=None)
    isHouseOpen = mongoengine.BooleanField(default=False)

    meta = {
        "collection": "runningInfo"
    }
