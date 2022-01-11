import json


def generate_running_info(show_id=None, session_id=None, is_house_open=False):
    return json.dumps({
        "showId": show_id,
        "sessionId": session_id,
        "isHouseOpen": is_house_open
    })
