from data.show import Show
from data.session import Session
from bson.objectid import ObjectId


def create_show(en_title: str, cn_title: str, duration_mins: int, default_rooms: list) -> Show:
    show = Show()
    show.enTitle = en_title
    show.cnTitle = cn_title
    show.durationMins = duration_mins
    show.defaultRooms = default_rooms

    show.save()
    return show


def get_show_dict(show: Show) -> dict:
    return {
        "enTitle": show.enTitle,
        "cnTitle": show.cnTitle,
        "durationMins": show.durationMins,
        "defaultRooms": show.defaultRooms,
        "id": str(show.id),
    }


def list_shows():
    return Show.objects()


def find_shows_id(search: str):
    query = list(Show.objects(id=ObjectId(search)))
    return query


def find_shows(search: str):
    query = list(Show.objects(enTitle=search))
    query.extend(list(Show.objects(cnTitle=search)))
    return query


def create_session(date_time: str, event_id: str, is_playing: bool, rooms: list) -> Session:
    session = Session()
    session.dateTime = date_time
    session.eventId = event_id
    session.isPlaying = is_playing
    session.rooms = rooms

    session.save()
    return session
