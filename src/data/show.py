import mongoengine

from data.room import Room


class Show(mongoengine.Document):
    enTitle = mongoengine.StringField(unique=True, required=True)
    cnTitle = mongoengine.StringField()
    durationMins = mongoengine.IntField()
    defaultRooms = mongoengine.EmbeddedDocumentListField(Room)

    meta = {
        "collection": "shows"
    }
