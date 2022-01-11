import json


show_a = json.dumps({
    "enTitle": "The Culprit",
    "cnTitle": "口癖",
    "durationMins": 120,
    "defaultRooms": [
        {"title": "Round Table", "url": "test", "isUnlocked": False},
        {"title": "Cashier Counter", "url": "test", "isUnlocked": False},
        {"title": "Noodles Stall", "url": "test", "isUnlocked": False},
        {"title": "Back Alley", "url": "test", "isUnlocked": False}
    ]
})


show_b = json.dumps({
    "enTitle": "The B",
    "cnTitle": "太好了",
    "durationMins": 100,
    "defaultRooms": [
        {"title": "Round Table", "url": "test", "isUnlocked": False},
        {"title": "Cashier Counter", "url": "test", "isUnlocked": False},
        {"title": "Noodles Stall", "url": "test", "isUnlocked": False},
        {"title": "Back Alley", "url": "test", "isUnlocked": False}
    ]
})


show_a_edit_en_title = json.dumps({
    "enTitle": "The Instigator",
})
