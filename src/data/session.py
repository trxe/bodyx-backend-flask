import datetime
import mongoengine
from data.room import Room


class Session(mongoengine.Document):
    dateTime = mongoengine.DateTimeField(default=datetime.datetime.now(), unique=True, required=True)
    eventId = mongoengine.StringField(required=True)
    isPlaying = mongoengine.BooleanField(default=False, required=True)
    showId = mongoengine.ObjectIdField(required=True)
    rooms = mongoengine.EmbeddedDocumentListField(Room)

    meta = {
        "collection": "sessions"
    }
