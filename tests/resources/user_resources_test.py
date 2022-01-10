import json
import unittest
import requests

import sample_data.user_sample as users


class TestUserResources(unittest.TestCase):
    root = "http://127.0.0.1:5000/"
    json_header = {"Content-type": "application/json", "x-access-token": None}

    @staticmethod
    def login():
        user_admin = json.loads(users.admin)
        res = requests.post(TestUserResources.root + "users", users.admin, headers=TestUserResources.json_header)
        auth_details = (user_admin["username"], user_admin["password"])
        response = requests.get(TestUserResources.root + "login", auth=auth_details)
        token = response.json().get("data").get("token")
        return user_admin, token
