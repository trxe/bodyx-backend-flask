import dateutil.parser
import mongoengine.errors

import services.data_service as svc
from data.session import Session
from commands.room_handlers import generate_room_list


def print_session(session: Session):
    show = svc.find_shows_id(session.showId)
    print(f" * {session.dateTime} (event: {session.eventId}; ",
          f"show: {show.enTitle if show else 'NOT FOUND'}) -- {session.id}")
    for r in session.rooms:
        print(f"   - [{'x' if r.isUnlocked else ' '}] {r.title} -- {r.url}")


def create_session():
    date_time = dateutil.parser.parse(input("enter date time [yyyy-mm-dd hh:mm]: "))
    event_id = input("enter eventbrite event id: ")
    show_id = input("enter show id: ")
    try:
        session = svc.create_session(date_time, event_id, show_id)
        print("show created:", str(session.id))
    except mongoengine.errors.NotUniqueError:
        print("Error: show with identical english title found")


def list_sessions():
    sessions = svc.list_sessions()
    print("sessions: ")
    for session in sessions:
        print_session(session)


def list_sessions_by_show():
    search = input("enter a show id: ")
    sessions = svc.list_sessions_by_show(search)
    print("sessions: ")
    for session in sessions:
        print_session(session)


def create_session_room():
    search = input("enter a session id: ")
    session = svc.find_session_id(search)
    room = generate_room_list()
    svc.create_session_rooms(session, room)
