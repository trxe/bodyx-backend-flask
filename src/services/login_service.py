import bcrypt
import uuid

from data.user import User
from exceptions.exceptions import NotFoundError


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def create_user(username: str, password: str, is_admin: bool) -> User:
    hashed_password = hash_password(password)
    user = User()
    user.publicId = uuid.uuid4()
    user.username = username
    user.password = hashed_password
    user.isAdmin = is_admin

    user.save()
    return user


def get_user_dict(user: User) -> dict:
    return {
        "username": user.username,
        "publicId": str(user.publicId),
        "isAdmin": user.isAdmin,
    }


def list_users() -> list:
    return list(User.objects())


def find_user(user_id=None, username=None) -> User:
    if user_id is not None:
        query = User.objects(publicId=uuid.UUID(user_id))
    else:
        query = User.objects(username=username)
    if len(query) == 0:
        raise NotFoundError(f"Show with id {user_id} not found")
    return query[0]


def update_user(user: User, username=None, password=None, is_admin=None) -> None:
    if username is not None:
        user.username = username
    if password is not None:
        user.password = hash_password(password)
    if is_admin is not None:
        user.isAdmin = is_admin

    user.save()
    return user


def reset_users() -> None:
    User.drop_collection()


def delete_user(user_id=None, username=None) -> None:
    user = find_user(user_id, username)
    user.delete()
