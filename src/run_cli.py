import mongoengine.errors

import services.data_service as svc
from data.mongo_setup import global_init
from data.show import Show
from dotenv import load_dotenv


def print_cmds():
    print("Welcome to BODYX services")
    print("[show] [session] -c: create show/session")
    print("[show] [session] -r: find show/session")
    # print("[show] [session] -u: update show/session")
    # print("[show] [session] -d: delete show/session")
    print("[show] [session] -l: list shows/session")
    print("[quit]")


def parse_cmds(raw: str):
    if raw == "start":
        return True
    cmd = raw.split(sep=" -")
    if cmd[0] == "":
        return True
    elif cmd[0] == "quit":
        return False
    elif len(cmd) == 1:
        print("cmd not found")
    elif cmd[1] == "c":
        create_show()
    elif cmd[1] == "r":
        find_show()
    elif cmd[1] == "l":
        list_shows()
    else:
        print("cmd not found")
    return True


def print_show(show: Show):
    print(f" * {show.enTitle} {show.cnTitle} {show.durationMins} mins -- {show.id}")


def generate_room():
    is_adding = input("add new room? [Y/N] ")
    if is_adding == "N":
        return None
    room_name = input("enter room name: ")
    room_url = input("enter url: ")
    return {"roomName": room_name, "roomUrl": room_url}


def create_show():
    en_title = input("enter english title: ")
    cn_title = input("enter chinese title: ")
    duration_mins = input("enter duration in minutes: ")
    print("enter default rooms: ")
    rooms = []
    try:
        show = svc.create_show(en_title, cn_title, duration_mins, rooms)
        print("show created:", show)
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


def main():
    load_dotenv()
    global_init()
    print_cmds()
    cmd = "start"
    while parse_cmds(cmd):
        cmd = input("> ")
