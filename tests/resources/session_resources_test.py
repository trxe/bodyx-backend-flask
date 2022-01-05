import json
import unittest
import requests
import dateutil.parser

import sample_data.show_sample as shows
import sample_data.session_sample as sessions


class TestSessionResources(unittest.TestCase):
    root = "http://127.0.0.1:5000/"
    json_header = {"Content-type": "application/json"}
    show_id = None
    show_rooms = None

    @classmethod
    def setUpClass(cls) -> None:
        requests.delete(TestSessionResources.root + "shows")
        response = requests.post(TestSessionResources.root + "shows", shows.show_a,
                                 headers=TestSessionResources.json_header)
        TestSessionResources.show_id = response.json()["data"]["id"]
        TestSessionResources.show_rooms = response.json()["data"]["defaultRooms"]

    def test_valid_post(self):
        requests.delete(TestSessionResources.root + "sessions")
        new_session = sessions.session_a(TestSessionResources.show_id)
        response = requests.post(TestSessionResources.root + "sessions", new_session,
                                 headers=TestSessionResources.json_header)
        new_session = response.json()["data"]
        new_session_rooms = new_session.pop("rooms")
        new_session.pop("id")
        expected_session = json.loads(sessions.session_a(TestSessionResources.show_id))
        expected_dt = dateutil.parser.parse(expected_session.pop("dateTime"))
        new_dt = dateutil.parser.parse(new_session.pop("dateTime"))
        self.assertEqual(False, new_session.pop("isPlaying"))
        self.assertEqual(expected_dt, new_dt)
        self.assertDictEqual(expected_session, new_session)
        self.assertListEqual(TestSessionResources.show_rooms, new_session_rooms)
        self.assertEqual(201, response.status_code)

    def test_fail_duplicate_post(self):
        TestSessionResources.test_valid_post(self)
        new_session = sessions.session_a(TestSessionResources.show_id)
        response = requests.post(TestSessionResources.root + "sessions", new_session,
                                 headers=TestSessionResources.json_header)
        self.assertIsNotNone(response.json()["error"])
        print(response.json()["error"])
        self.assertEqual(400, response.status_code)

    def test_get(self):
        TestSessionResources.test_valid_post(self)
        response = requests.get(TestSessionResources.root + "sessions")
        session_to_find = response.json().get("data")[0]
        print(response.json())
        response = requests.get(TestSessionResources.root + "sessions/" + session_to_find["id"])
        print(response.json())
        response = requests.get(TestSessionResources.root + "sessions?show_id=" + TestSessionResources.show_id)
        print(response.json())
        self.assertEqual(200, response.status_code)

    def test_put_toggle_play(self):
        TestSessionResources.test_valid_post(self)
        session_list = requests.get(TestSessionResources.root + "sessions").json().get("data")
        session_to_edit = session_list[0]
        response = requests.put(TestSessionResources.root + "sessions/" + session_to_edit["id"],
                                sessions.session_edit_is_playing, headers=TestSessionResources.json_header)
        new_session = response.json()["data"]
        expected_session = session_to_edit
        expected_session["isPlaying"] = True
        self.assertDictEqual(expected_session, new_session)
        self.assertEqual(201, response.status_code)
        response = requests.put(TestSessionResources.root + "sessions/" + session_to_edit["id"],
                                sessions.session_edit_stop_playing, headers=TestSessionResources.json_header)
        new_session = response.json()["data"]
        expected_session = session_to_edit
        expected_session["isPlaying"] = False
        self.assertDictEqual(expected_session, new_session)
        self.assertEqual(201, response.status_code)

    def test_put_update_rooms(self):
        TestSessionResources.test_valid_post(self)
        session_list = requests.get(TestSessionResources.root + "sessions").json().get("data")
        session_to_edit = session_list[0]
        response = requests.put(TestSessionResources.root + "sessions/" + session_to_edit["id"],
                                sessions.session_edit_rooms, headers=TestSessionResources.json_header)
        new_session = response.json()["data"]
        expected_session = session_to_edit
        expected_session["rooms"] = json.loads(sessions.session_edit_rooms).pop("rooms")
        self.assertDictEqual(expected_session, new_session)
        self.assertEqual(201, response.status_code)

    def test_delete(self) -> None:
        TestSessionResources.test_valid_post(self)
        session_list = requests.get(TestSessionResources.root + "sessions").json().get("data")
        session_to_delete = session_list[0]
        response = requests.delete(TestSessionResources.root + "sessions/" + session_to_delete.get("id"))
        self.assertEqual(204, response.status_code)

    def test_fail_delete_invalid_id(self) -> None:
        requests.delete(TestSessionResources.root + "sessions")
        response = requests.delete(TestSessionResources.root + "sessions/61d53ae30c85f2bb05c085a5")
        self.assertEqual(404, response.status_code)
