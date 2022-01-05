import unittest
from resources.response import Response


class TestResponse(unittest.TestCase):
    def test_to_json(self):
        r = Response(msg="Welcome!", data={"test": 2, "test2": {"nested": "data"}})
        r_json = r.to_json()
        print(r_json)
        self.assertEqual(type(r_json), dict)
