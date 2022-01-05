def generate_room():
    is_adding = input("add new room? [Y/N] ")
    if is_adding == "Y" or is_adding == "y":
        room_name = input("enter room name: ")
        room_url = input("enter url: ")
        return {"title": room_name, "url": room_url}
    else:
        return None


def generate_room_list():
    rooms, is_adding = [], True
    while is_adding:
        room = generate_room()
        if room:
            rooms.append(room)
        else:
            is_adding = False
    return rooms
