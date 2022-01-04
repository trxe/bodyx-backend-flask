from data.show import Show
import services.data_service as svc
import mongoengine


def print_show(show: Show):
    print(f" * {show.enTitle} {show.cnTitle} {show.durationMins} mins -- {show.id}")


def create_show():
    en_title = input("enter english title: ")
    cn_title = input("enter chinese title: ")
    duration_mins = int(input("enter duration in minutes: "))
    print("enter default rooms: ")
    try:
        show = svc.create_show(en_title, cn_title, duration_mins, default_rooms=[])
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
