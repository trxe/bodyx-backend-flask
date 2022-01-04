import datetime
import mongoengine
from data.room import Room


class Session(mongoengine.Document):
    dateTime = mongoengine.DateTimeField(default=datetime.datetime.now(), required=True)
    eventId = mongoengine.StringField(required=True)
    isPlaying = mongoengine.BooleanField(default=False, required=True)
    rooms = mongoengine.EmbeddedDocumentListField(Room)

    meta = {
        "db_alias": "core",
        "collection": "sessions"
    }
