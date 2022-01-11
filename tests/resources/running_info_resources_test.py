import json
import unittest
import requests

import sample_data.show_sample as shows
import sample_data.session_sample as sessions
import sample_data.running_info_sample as running_info
from resources.user_resources_test import TestUserResources


class TestRunningInfoResources(unittest.TestCase):
    root = "http://127.0.0.1:5000/"
    json_header = {"Content-type": "application/json", "x-access-token": None}
    user = None
    show_id = None
    session_id = None

    @classmethod
    def setUpClass(cls) -> None:
        TestRunningInfoResources.user, token = TestUserResources.login()
        TestRunningInfoResources.json_header["x-access-token"] = token
        requests.delete(TestRunningInfoResources.root + "shows",
                        headers=TestRunningInfoResources.json_header)
        requests.delete(TestRunningInfoResources.root + "sessions",
                        headers=TestRunningInfoResources.json_header)
        response = requests.post(TestRunningInfoResources.root + "shows", shows.show_a,
                                 headers=TestRunningInfoResources.json_header)
        TestRunningInfoResources.show_id = response.json()["data"]["id"]
        new_session = sessions.session_a(TestRunningInfoResources.show_id)
        response = requests.post(TestRunningInfoResources.root + "sessions", new_session,
                                 headers=TestRunningInfoResources.json_header)
        TestRunningInfoResources.session_id = response.json()["data"]["id"]

    def test_reset(self):
        requests.delete(TestRunningInfoResources.root + "runningInfo",
                        headers=TestRunningInfoResources.json_header)
        info = requests.get(TestRunningInfoResources.root + "runningInfo",
                            headers=TestRunningInfoResources.json_header).json().get("data")
        self.assertDictEqual({"show": None, "session": None, "isHouseOpen": False}, info)

    def test_valid_post(self):
        self.test_reset()
        info = running_info.generate_running_info(TestRunningInfoResources.show_id,
                                                  TestRunningInfoResources.session_id,
                                                  is_house_open=True)
        response = requests.post(TestRunningInfoResources.root + "runningInfo", info,
                                 headers=TestRunningInfoResources.json_header)
        update_info = response.json().get("data")
        show = update_info.get("show")
        show_res = requests.get(TestRunningInfoResources.root + "shows/" +
                                TestRunningInfoResources.show_id,
                                headers=TestRunningInfoResources.json_header)
        self.assertEqual(show_res.json().get("data"), show)
        session = update_info.get("session")
        sessions_res = requests.get(TestRunningInfoResources.root + "sessions/" +
                                    TestRunningInfoResources.session_id,
                                    headers=TestRunningInfoResources.json_header)
        self.assertEqual(sessions_res.json().get("data"), session)
        self.assertEqual(True, update_info.get("isHouseOpen"))

    def test_valid_update(self):
        self.test_valid_post()
        new_show = requests.post(TestRunningInfoResources.root + "shows", shows.show_b,
                                 headers=TestRunningInfoResources.json_header).json().get("data")
        new_session = requests.post(TestRunningInfoResources.root + "sessions", sessions.session_b(new_show.get("id")),
                                    headers=TestRunningInfoResources.json_header).json().get("data")
        info = running_info.generate_running_info(new_show.get("id"), new_session.get("id"), is_house_open=True)
        response = requests.post(TestRunningInfoResources.root + "runningInfo", info,
                                 headers=TestRunningInfoResources.json_header)
        update_info = response.json().get("data")
        show = update_info.get("show")
        self.assertEqual(new_show, show)
        session = update_info.get("session")
        self.assertEqual(new_session.get("id"), session.get("id"))
        self.assertEqual(True, session.get("isPlaying"))
        self.assertEqual(True, update_info.get("isHouseOpen"))
        sessions_res = requests.get(TestRunningInfoResources.root + "sessions/" +
                                    TestRunningInfoResources.session_id,
                                    headers=TestRunningInfoResources.json_header)
        self.assertEqual(False, sessions_res.json().get("data").get("isPlaying"))
