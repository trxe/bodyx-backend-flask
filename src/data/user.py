import mongoengine


class User(mongoengine.Document):
    email = mongoengine.StringField(required=True)
    username = mongoengine.StringField(required=True)
    publicId = mongoengine.UUIDField(required=True)
    password = mongoengine.BinaryField(required=True)
    isAdmin = mongoengine.BooleanField(default=False)
    isLoggedIn = mongoengine.BooleanField(default=False)

    meta = {
        "collection": "users"
    }
