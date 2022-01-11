import json


def session_a(show_id):
    return json.dumps({
        "dateTime": "2012-01-01T23:30:00+02:00",
        "eventId": "first",
        "showId": show_id,
    })


def session_b(show_id):
    return json.dumps({
        "dateTime": "2017-01-01T23:30:00+08:00",
        "eventId": "second",
        "showId": show_id,
    })


session_edit_is_playing = json.dumps({
    "isPlaying": True
})


session_edit_stop_playing = json.dumps({
    "isPlaying": False
})


session_edit_rooms = json.dumps({
    "rooms": [
        {
            "title": "Round Chair",
            "url": "Boo",
            "isUnlocked": True,
        }
    ]
})