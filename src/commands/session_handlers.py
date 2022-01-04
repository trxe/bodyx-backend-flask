import dateutil.parser
import mongoengine.errors

import services.data_service as svc
from data.session import Session


def print_session(session: Session):
    show = svc.find_shows_id(session.showId)
    print(f" * {session.dateTime} (event: {session.eventId}; ",
          f"show: {show.enTitle if show else 'NOT FOUND'}) -- {session.id}")


def generate_room():
    is_adding = input("add new room? [Y/N] ")
    if is_adding == "N":
        return None
    room_name = input("enter room name: ")
    room_url = input("enter url: ")
    return {"roomName": room_name, "roomUrl": room_url}


def create_session():
    date_time = dateutil.parser.parse(input("enter date time [yyyy-mm-dd]: "))
    event_id = input("enter eventbrite event id: ")
    show_id = input("enter show id: ")
    print("enter rooms: ")
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
