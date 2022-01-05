from flask import request
from flask_restful import Resource

import services.data_service as svc
from resources.response import error_json, success_json
from exceptions.exceptions import NotFoundError, InvalidIdError


def retrieve_show_args(args) -> tuple:
    en_title = args.get("enTitle")
    cn_title = args.get("cnTitle")
    duration_mins = args.get("durationMins")
    default_rooms = args.get("defaultRooms")
    return en_title, cn_title, duration_mins, default_rooms


class Show(Resource):
    @staticmethod
    def get(show_id=None):
        if show_id is not None:
            try:
                shows = svc.list_sessions_by_show(show_id)
                return success_json("Found show", list(map(svc.get_show_dict, shows)))
            except NotFoundError as e:
                return error_json(e), 404
            except InvalidIdError as e:
                return error_json(e), 403
        return success_json("Found shows:", list(map(svc.get_show_dict, svc.list_shows())))

    @staticmethod
    def post():
        try:
            args = request.json
            en_title, cn_title, duration_mins, default_rooms = retrieve_show_args(args)
            show = svc.create_show(en_title, cn_title, duration_mins, default_rooms)
            return success_json(f"Created new show {show.id}", svc.get_show_dict(show)), 201
        except Exception as e:
            return error_json(e), 400

    @staticmethod
    def put(show_id):
        try:
            show = svc.find_show_id(show_id)
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 403
        args = request.json
        en_title, cn_title, duration_mins, default_rooms = retrieve_show_args(args)
        try:
            svc.update_show(show, en_title, cn_title, duration_mins, default_rooms)
        except Exception as e:
            return error_json(e), 400
        return success_json(f"Edited show {show.id}", svc.get_show_dict(show)), 201

    @staticmethod
    def delete(show_id=None):
        if not show_id:
            svc.reset_shows()
        try:
            svc.delete_show(show_id)
        except NotFoundError as e:
            return error_json(e), 404
        return None, 204
