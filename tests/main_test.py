import unittest
from mongoengine import connect, disconnect
import run_cli
import services.data_service as svc


class TestRunCli(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDown(cls) -> None:
        disconnect()

    def test_list_shows(self):
        svc.create_show("showA", "cnA", 100, [])
        svc.create_show("showB", "cnB", 120, [])
        run_cli.list_shows()
