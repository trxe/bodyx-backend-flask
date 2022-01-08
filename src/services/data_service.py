import bson.errors
from bson.objectid import ObjectId
import copy
import datetime

from data.show import Show
from data.session import Session
from data.room import Room
from exceptions.exceptions import NotFoundError, InvalidIdError


def reset_shows() -> None:
    Show.drop_collection()


def reset_sessions() -> None:
    Session.drop_collection()


def create_show(en_title: str, cn_title: str, duration_mins: int, default_rooms: list[dict]) -> Show:
    show = Show()
    show.enTitle = en_title
    show.cnTitle = cn_title
    show.durationMins = duration_mins
    for rawRoom in default_rooms:
        room = Room()
        room.title = rawRoom.get("title")
        room.url = rawRoom.get("url")
        room.isUnlocked = rawRoom.get("isUnlocked")
        show.defaultRooms.append(room)

    print(show.to_json())
    show.save()
    return show


def update_show(show: Show, en_title=None, cn_title=None, duration_mins=None, default_rooms=None) -> Show:
    if en_title is not None:
        show.enTitle = en_title
    if cn_title is not None:
        show.cnTitle = cn_title
    if duration_mins is not None:
        show.durationMins = duration_mins
    if default_rooms is not None:
        show.defaultRooms = []
        for rawRoom in default_rooms:
            room = Room()
            room.title = rawRoom["title"]
            room.url = rawRoom["url"]
            show.defaultRooms.append(room)

    show.save()
    return show


def get_room_dict(room: Room) -> dict:
    return {
        "title": room.title,
        "url": room.url,
        "isUnlocked": room.isUnlocked,
    }


def get_show_dict(show: Show) -> dict:
    return {
        "enTitle": show.enTitle,
        "cnTitle": show.cnTitle,
        "durationMins": show.durationMins,
        "defaultRooms": list(map(get_room_dict, show.defaultRooms)),
        "id": str(show.id),
    }


def get_session_dict(session: Session) -> dict:
    return {
        "dateTime": str(session.dateTime),
        "eventId": session.eventId,
        "isPlaying": session.isPlaying,
        "showId": str(session.showId),
        "rooms": list(map(get_room_dict, session.rooms)),
        "id": str(session.id),
    }


def list_shows() -> list:
    return list(Show.objects())


def delete_show(show_id: str) -> None:
    show = find_show_id(show_id)
    show.delete()


def find_show_id(search: str) -> Show:
    try:
        query = list(Show.objects(id=ObjectId(search)))
    except bson.errors.InvalidId as e:
        raise InvalidIdError(invalid_id=search)
    if len(query) == 0:
        raise NotFoundError(f"Show with id {search} not found")
    return query[0]


def find_shows(search: str) -> list:
    query = list(Show.objects(enTitle=search))
    query.extend(list(Show.objects(cnTitle=search)))
    return query


def create_session(date_time: datetime, event_id: str, show_id: str) -> Session:
    session = Session()
    session.dateTime = date_time
    session.eventId = event_id
    session.showId = ObjectId(show_id)
    session.isPlaying = False

    show = find_show_id(show_id)
    session.rooms = copy.deepcopy(show.defaultRooms)

    session.save()
    return session


def create_session_rooms(session: Session, rooms: list[dict]) -> Session:
    for rawRoom in rooms:
        room = Room()
        room.title = rawRoom.get("title")
        room.url = rawRoom.get("url")
        room.isUnlocked = rawRoom.get("isUnlocked")
        session.rooms.append(room)

    session.save()
    return session


def update_session(session: Session, date_time=None, event_id=None, is_playing=None,
                   show_id=None, updated_rooms=None) -> None:
    if date_time is not None:
        session.dateTime = date_time
    if event_id is not None:
        session.eventId = event_id
    if is_playing is not None:
        session.isPlaying = is_playing
    if show_id is not None:
        session.showId = show_id
    if updated_rooms is not None:
        session.rooms = []
        for rawRoom in updated_rooms:
            room = Room()
            room.title = rawRoom.get("title")
            room.url = rawRoom.get("url")
            room.isUnlocked = rawRoom.get("isUnlocked")
            session.rooms.append(room)

    session.save()
    return session


def list_sessions() -> list:
    return list(Session.objects())


def list_sessions_by_show(search: str) -> list:
    return list(Session.objects(showId=ObjectId(search)))


def find_session_id(search: str) -> Session:
    try:
        query = list(Session.objects(id=ObjectId(search)))
    except bson.errors.InvalidId as e:
        raise InvalidIdError(invalid_id=search)
    if len(query) == 0:
        raise NotFoundError(f"Show with id {search} not found")
    return query[0]


def delete_session(session_id):
    session = find_session_id(session_id)
    session.delete()
