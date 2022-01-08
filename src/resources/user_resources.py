from flask import request
from flask_restful import Resource
from functools import wraps
import jwt
import os.path

import services.login_service as login_svc
from resources.response import error_json, success_json
from exceptions.exceptions import NotFoundError, InvalidIdError, InvalidTokenError, NoAccessError


secret_key = os.getenv("SECRET_KEY")


def retrieve_user_args(args) -> tuple:
    username = args.get("username")
    password = args.get("password")
    is_admin = args.get("isAdmin")
    session_id = args.get("sessionId")
    return username, password, is_admin, session_id


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "x-access-token" not in request.headers:
            return error_json(InvalidTokenError(missing=True)), 401
        try:
            token = request.headers.get("x-access-token")
            print("User token:", str(token))
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = login_svc.find_user(user_id=data["publicId"])
        except NotFoundError:
            return error_json(InvalidTokenError()), 401
        return f(current_user, *args, **kwargs)

    return decorated


class User(Resource):
    @staticmethod
    @token_required
    def get(current_user, user_id=None):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        try:
            if not user_id:
                users = login_svc.list_users()
                return success_json("Found users", list(map(login_svc.get_user_dict, users)))
            else:
                user = login_svc.find_user(user_id)
                return success_json("Found user", login_svc.get_user_dict(user))
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 400

    @staticmethod
    def post():
        try:
            args = request.json
            username, password, is_admin, session_id = retrieve_user_args(args)
            user = login_svc.create_user(username, password, is_admin, session_id)
            return success_json(f"Created new user {user.id}", login_svc.get_user_dict(user)), 201
        except Exception as e:
            return error_json(e), 400

    @staticmethod
    @token_required
    def put(current_user, user_id):
        if not current_user:
            return error_json(NoAccessError()), 401

        try:
            user = login_svc.find_user(user_id=user_id)
        except NotFoundError as e:
            return error_json(e), 404
        args = request.json
        username, password, is_admin = retrieve_user_args(args)
        try:
            login_svc.update_user(user, username, password, is_admin)
        except Exception as e:
            return error_json(e), 400
        return success_json(f"Edited user {user_id}", login_svc.get_user_dict(user)), 201

    @staticmethod
    @token_required
    def delete(current_user, user_id=None):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        if not user_id:
            login_svc.reset_users()
        try:
            login_svc.delete_user(user_id)
        except NotFoundError as e:
            return error_json(e), 404
        return None, 204
