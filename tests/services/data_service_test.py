import unittest
from mongoengine import connect, disconnect
import services.data_service as svc
from data.show import Show


class TestDataService(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDown(cls) -> None:
        disconnect()

    def test_create_show(self):
        print("===========")
        print("Create Show")
        show = svc.create_show("enTitle", "cnTitle", 120, [])
        fresh_show = Show.objects().first()
        self.assertEqual(fresh_show, show, "create ok")

    def test_list_show(self):
        print("===========")
        print("List Show")
        show_a = svc.create_show("showA", "cnA", 100, [])
        show_b = svc.create_show("showB", "cnB", 120, [])
        show_list = [{
            "enTitle": show_a.enTitle,
            "cnTitle": show_a.cnTitle,
            "durationMins": show_a.durationMins,
            "defaultRooms": show_a.defaultRooms,
        }, {
            "enTitle": show_b.enTitle,
            "cnTitle": show_b.cnTitle,
            "durationMins": show_b.durationMins,
            "defaultRooms": show_b.defaultRooms,
        }]
        db_show_list = list(map(svc.get_show_dict, svc.list_shows()))
        for s in db_show_list:
            print("show id:", s["id"], type(s["id"]))
            s.pop("id")
        self.assertListEqual(show_list, db_show_list, "list ok")

    def test_find_show(self):
        print("===========")
        print("Find Show by Title")
        show_a = svc.create_show("showA", "cnA", 100, [])
        show_b = svc.create_show("showB", "cnB", 120, [])
        show_search = svc.find_shows("showA")
        for s in show_search:
            print(f"{s.id}: {s.enTitle} {s.cnTitle}, {s.durationMins}")
        self.assertEqual(show_a, show_search[0])

    def test_find_show_id(self):
        print("===========")
        print("Find Show by Id")
        show_a = svc.create_show("showA", "cnA", 100, [])
        show_b = svc.create_show("showB", "cnB", 120, [])
        show_search_id = svc.find_shows("showB")[0].id
        print("search id:", show_search_id)
        show_search = svc.find_shows_id(show_search_id)
        for s in show_search:
            print(f"{s.id}: {s.enTitle} {s.cnTitle}, {s.durationMins}")
        self.assertEqual(show_b, show_search[0])
