import mongoengine

from data.show import Show
import services.data_service as svc
from commands.room_handlers import generate_room_list


def print_show(show: Show):
    print(f" * {show.enTitle} {show.cnTitle} {show.durationMins} mins -- {show.id}")


def create_show():
    en_title = input("enter english title: ")
    cn_title = input("enter chinese title: ")
    duration_mins = int(input("enter duration in minutes: "))
    print("enter default rooms: ")
    rooms = generate_room_list()
    try:
        show = svc.create_show(en_title, cn_title, duration_mins, default_rooms=rooms)
        print("show created:", str(show.id))
    except mongoengine.errors.NotUniqueError:
        print("Error: show with identical english title found")


def find_show():
    title = input("enter title to search: ")
    shows_found = svc.find_shows(title)
    if len(shows_found) == 0:
        print(f"no shows found with title {title}")
        return
    print("shows: ")
    for show in shows_found:
        print_show(show)


def list_shows():
    shows = svc.list_shows()
    print("shows: ")
    for show in shows:
        print_show(show)


def delete_show():
    delete_id = input("enter show id to delete: ")
    try:
        svc.delete_show(delete_id)
    except Exception as e:
        print("[ERROR] show not found:", e)


def find_show_id():
    show_id = input("enter show id to search: ")
    try:
        show_found = svc.find_show_id(show_id)
        print("shows:")
        print_show(show_found)
    except Exception as e:
        print("[ERROR] show not found:", e)
