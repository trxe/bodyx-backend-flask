from dotenv import load_dotenv

import commands.show_handlers as show_cmd
import commands.session_handlers as session_cmd
from data.mongo_setup import global_init


def print_cmds():
    print("Welcome to BODYX services")
    print("[show] [session] -c: create show/session")
    print("[show] [session] -r: find show/session")
    print("session -u --room -c: create room for this session")
    print("session -u --room -u: update room for this session")
    # print("[show] [session] -d: delete show/session")
    print("[show] [session] -l: list shows/session")
    print("help: shows this page")
    print("quit")


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
    elif cmd[0] == "show":
        if cmd[1] == "c":
            show_cmd.create_show()
        elif cmd[1] == "r":
            if cmd[2] == "-id":
                show_cmd.find_show_id()
            elif cmd[2] == "-title":
                show_cmd.find_show()
        elif cmd[1] == "d":
            show_cmd.delete_show()
        elif cmd[1] == "l":
            show_cmd.list_shows()
    elif cmd[0] == "help":
        print_cmds()
    elif cmd[0] == "session":
        if cmd[1] == "c":
            session_cmd.create_session()
        elif cmd[1] == "r":
            session_cmd.list_sessions_by_show()
        elif cmd[1] == "u":
            if cmd[2] == "-room" and cmd[3] == "c":
                session_cmd.create_session_room()
            elif cmd[2] == "-room" and cmd[3] == "u":
                print("update room")
        elif cmd[1] == "l":
            session_cmd.list_sessions()
    else:
        print("cmd not found")
    return True


def main():
    load_dotenv()
    global_init()
    print_cmds()
    cmd = "start"
    while parse_cmds(cmd):
        cmd = input("> ")
