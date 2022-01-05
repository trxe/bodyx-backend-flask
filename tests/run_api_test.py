import unittest
import requests

import sample_data.show_sample as shows


class TestRunApi(unittest.TestCase):
    root = "http://127.0.0.1:5000/"

    def test_get(self) -> None:
        response = requests.get(TestRunApi.root + "shows")
        print(response.json())
        response = requests.get(TestRunApi.root + "shows/" + "0")
        print(response.json())

    def test_post(self) -> None:
        response = requests.post(TestRunApi.root + "shows", shows.show_a)
        print(response.json())

    def test_post(self) -> None:
        response = requests.post(TestRunApi.root + "shows", shows.show_a)
        print(response.json())
