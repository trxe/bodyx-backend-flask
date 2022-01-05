import mongoengine


class Room(mongoengine.EmbeddedDocument):
    title = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    isUnlocked = mongoengine.BooleanField(default=False, required=True)
