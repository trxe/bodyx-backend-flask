from data.show import Show
from data.session import Session
from bson.objectid import ObjectId
import datetime


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


def list_shows() -> list:
    return Show.objects()


def find_shows_id(search: str) -> Show:
    query = list(Show.objects(id=ObjectId(search)))
    if len(query) == 0:
        return None
    return query[0]


def find_shows(search: str) -> list:
    query = list(Show.objects(enTitle=search))
    query.extend(list(Show.objects(cnTitle=search)))
    return query


def create_session(date_time: datetime, event_id: str, show_id: str,
                   is_playing: bool = False) -> Session:
    session = Session()
    session.dateTime = date_time
    session.eventId = event_id
    session.showId = ObjectId(show_id)
    session.isPlaying = is_playing
    session.rooms = []

    session.save()
    return session


def list_sessions():
    return Session.objects()


def list_sessions_by_show(search: str):
    return Session.objects(showId=ObjectId(search))
