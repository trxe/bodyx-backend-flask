import unittest

from mongoengine import connect, disconnect
import services.login_service as svc
from data.user import User


class TestLoginService(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDown(cls) -> None:
        disconnect()

    def test_create_user(self):
        print("Create User")
        user = svc.create_user("admin", "password", False)
        fresh_user = User.objects().first()
        print(f"{fresh_user.username} ({fresh_user.publicId}): {fresh_user.password}")
        self.assertEqual(fresh_user, user)

    def test_find_user_id(self):
        print("Find User by Id")
        user_a = svc.create_user("admin", "passwordIsDumb", True)
        print("search username: admin" )
        user = svc.find_user(username="admin")
        print(f"{user.username} ({user.publicId}): {user.password}")
        self.assertEqual(user_a, user)

        user_b = svc.create_user("viewer", "passwordIsBad", False)
        user_search_id = svc.find_user(username="viewer").publicId
        print("search id:", user_search_id)
        user = svc.find_user(user_id=user_search_id)
        print(f"{user.username} ({user.publicId}): {user.password}")
        self.assertEqual(user_b, user)


