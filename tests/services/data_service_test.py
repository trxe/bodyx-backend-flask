import unittest

import dateutil.parser
from mongoengine import connect, disconnect
import services.data_service as svc
from data.show import Show
from data.session import Session


# TODO: test API
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
        show = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        fresh_show = Show.objects().first()
        self.assertEqual(fresh_show, show)

    def test_update_show(self):
        print("===========")
        print("Update Show")
        show = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        # update title
        svc.update_show(show, en_title="somethingGreater")
        self.assertEqual("somethingGreater", show.enTitle)
        # update mins
        svc.update_show(show, duration_mins=130)
        self.assertEqual(130, show.durationMins)
        # update default rooms
        updated_rooms = [{"title": "RT", "url": "lmao"}]
        svc.update_show(show, default_rooms=updated_rooms)
        self.assertEqual("lmao", show.defaultRooms[0].url)

    def test_delete_show(self):
        print("===========")
        print("Delete Show")
        show_a = svc.create_show("showA", "cnA", 100, [])
        show_b = svc.create_show("showB", "cnB", 120, [])
        show_c = svc.create_show("showC", "cnB", 130, [])
        svc.delete_show(show_b.id)
        final_shows = [show_a, show_c]
        show_list = svc.list_shows()
        self.assertListEqual(final_shows, show_list)

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
        s = svc.find_show_id(show_search_id)
        print(f"{s.id}: {s.enTitle} {s.cnTitle}, {s.durationMins}")
        self.assertEqual(show_b, s)

    def test_create_session(self):
        print("===========")
        print("Create Session")
        show_a = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        show_a_id = str(show_a.id)
        dt = dateutil.parser.parse("2022-01-03")
        session = svc.create_session(dt, "eventOne", show_a_id)
        fresh_session = Session.objects().first()
        print("session:", session.rooms[0].title, session.rooms[0].url)
        self.assertEqual(fresh_session, session, "create ok")

    def test_create_session_room(self):
        print("===========")
        print("Create Session Room")
        show_a = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        session = svc.create_session(dateutil.parser.parse("2022-01-03"), "eventOne", str(show_a.id))
        fresh_session = svc.create_session_rooms(session, [{"title": "CC", "url": "meme"}])
        self.assertEqual(fresh_session, session, "create ok")
        new_session_list = list(map(lambda r: {"title": r.title, "url": r.url}, session.rooms))
        expected_session_list = [{"title": "RT", "url": ""}, {"title": "CC", "url": "meme"}]
        self.assertEqual(new_session_list, expected_session_list)

    def test_update_session_room(self):
        print("===========")
        print("Update Session Room")
        show_a = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        session = svc.create_session(dateutil.parser.parse("2022-01-03"), "eventOne", str(show_a.id))
        fresh_session = svc.update_session(session, updated_rooms=[{"title": "CC", "url": "meme"}])
        self.assertEqual(fresh_session, session, "create ok")
        new_session_list = list(map(lambda r: {"title": r.title, "url": r.url}, session.rooms))
        expected_session_list = [{"title": "CC", "url": "meme"}]
        self.assertEqual(new_session_list, expected_session_list)

    def test_update_session(self):
        print("===========")
        print("Update Session")
        show_a = svc.create_show("enTitle", "cnTitle", 120, [{"title": "RT", "url": ""}])
        old_time = dateutil.parser.parse("2022-01-03")
        session = svc.create_session(old_time, "eventOne", str(show_a.id))
        # update time
        new_time = dateutil.parser.parse("2022-01-05 10:00")
        svc.update_session(session, date_time=new_time)
        self.assertEqual(new_time, session.dateTime)
        self.assertNotEqual(old_time, session.dateTime)

    def test_list_sessions_by_show(self):
        print("===========")
        print("List Session by show")
        show_a = svc.create_show("showA", "cnA", 100, [])
        show_b = svc.create_show("showB", "cnB", 120, [])
        show_a_id = str(show_a.id)
        show_b_id = str(show_b.id)
        dt = list(map(dateutil.parser.parse, ["2022-01-03", "2023-01-03", "2022-01-04"]))
        session_one = svc.create_session(dt[0], "first", show_a_id)
        session_two = svc.create_session(dt[1], "second", show_b_id)
        session_three = svc.create_session(dt[2], "third", show_a_id)
        sessions_a = svc.list_sessions_by_show(show_a_id)
        sessions_b = svc.list_sessions_by_show(show_b_id)
        self.assertListEqual(sessions_a, [session_one, session_three])
        self.assertListEqual(sessions_b, [session_two])
