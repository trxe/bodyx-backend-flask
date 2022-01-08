import os
import mongoengine
import certifi


def global_init():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_uri = f"mongodb+srv://trxe:{password}@trxe.xxx0v.mongodb.net/{db_name}?retryWrites=true&w=majority"
    print(f"Connecting to {db_name} (user: {user})")
    mongoengine.connect(db=db_name, username=user, password=password, host=db_uri, tlsCAFile=certifi.where())


def mock_init():
    mongoengine.connect('mongoenginetest', host='mongomock://localhost')
