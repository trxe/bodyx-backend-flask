import json
import unittest
import requests

import sample_data.show_sample as shows


class TestShowResources(unittest.TestCase):
    root = "http://127.0.0.1:5000/"
    json_header = {"Content-type": "application/json"}

    def test_valid_post(self) -> None:
        requests.delete(TestShowResources.root + "shows")
        response = requests.post(TestShowResources.root + "shows", shows.show_a,
                                 headers=TestShowResources.json_header)
        new_show = response.json()["data"]
        new_show_rooms = new_show.pop("defaultRooms")
        new_show.pop("id")
        expected_show = json.loads(shows.show_a)
        expected_show_rooms = expected_show.pop("defaultRooms")
        self.assertDictEqual(expected_show, new_show)
        self.assertListEqual(expected_show_rooms, new_show_rooms)
        self.assertEqual(201, response.status_code)

    def test_fail_duplicate_post(self) -> None:
        TestShowResources.test_valid_post(self)
        response = requests.post(TestShowResources.root + "shows", shows.show_a,
                                 headers=TestShowResources.json_header)
        self.assertIsNotNone(response.json()["error"])
        print(response.json()["error"])
        self.assertEqual(400, response.status_code)

    def test_get(self) -> None:
        TestShowResources.test_valid_post(self)
        response = requests.get(TestShowResources.root + "shows")
        print(response.json())
        self.assertEqual(200, response.status_code)

    def test_put(self) -> None:
        TestShowResources.test_valid_post(self)
        show_list = requests.get(TestShowResources.root + "shows").json().get("data")
        show_to_edit = show_list[0]
        response = requests.put(TestShowResources.root + "shows/" + show_to_edit["id"],
                                shows.show_a_edit_en_title, headers=TestShowResources.json_header)
        new_show = response.json()["data"]
        expected_show = show_to_edit
        expected_show["enTitle"] = json.loads(shows.show_a_edit_en_title)["enTitle"]
        self.assertDictEqual(expected_show, new_show)
        self.assertEqual(201, response.status_code)

    def test_fail_put_invalid_id(self) -> None:
        requests.delete(TestShowResources.root + "shows")
        response = requests.put(TestShowResources.root + "shows/" + "61d53ae30c85f2bb05c085a5",
                                shows.show_a_edit_en_title, headers=TestShowResources.json_header)
        self.assertEqual(404, response.status_code)
        response = requests.put(TestShowResources.root + "shows/" + "200",
                                shows.show_a_edit_en_title, headers=TestShowResources.json_header)
        self.assertEqual(400, response.status_code)

    def test_delete(self) -> None:
        TestShowResources.test_valid_post(self)
        show_list = requests.get(TestShowResources.root + "shows").json().get("data")
        show_to_delete = show_list[0]
        response = requests.delete(TestShowResources.root + "shows/" + show_to_delete.get("id"))
        self.assertEqual(204, response.status_code)

    def test_fail_delete_invalid_id(self) -> None:
        requests.delete(TestShowResources.root + "shows")
        response = requests.delete(TestShowResources.root + "shows/61d53ae30c85f2bb05c085a5")
        self.assertEqual(404, response.status_code)
