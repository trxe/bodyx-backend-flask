from flask import request
from flask_restful import Resource, inputs

import services.data_service as svc
from resources.response import error_json, success_json
from exceptions.exceptions import NotFoundError, InvalidIdError


def retrieve_session_args(args) -> tuple:
    date_time = None if not args.get("dateTime") else inputs.datetime_from_iso8601(args.get("dateTime"))
    event_id = args.get("eventId")
    show_id = args.get("showId")
    is_playing = args.get("isPlaying")
    rooms = args.get("rooms")
    return date_time, event_id, show_id, is_playing, rooms


class Session(Resource):
    @staticmethod
    def get(session_id=None):
        try:
            if session_id:
                session = svc.find_session_id(session_id)
                return success_json(f"found session with id {session_id}", svc.get_session_dict(session))
            elif request.args and "show_id" in request.args:
                sessions = svc.list_sessions_by_show(request.args.get("show_id"))
                return success_json("Found sessions:", list(map(svc.get_session_dict, sessions)))
            else:
                return success_json("Found sessions:", list(map(svc.get_session_dict, svc.list_sessions())))
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 403

    @staticmethod
    def post():
        try:
            args = request.json
            date_time, event_id, show_id, is_playing, rooms = retrieve_session_args(args)
            session = svc.create_session(date_time, event_id, show_id)
            return success_json(f"Created new session {session.id}", svc.get_session_dict(session)), 201
        except Exception as e:
            return error_json(e), 400

    @staticmethod
    def put(session_id):
        try:
            session = svc.find_session_id(session_id)
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 403
        try:
            args = request.json
            date_time, event_id, show_id, is_playing, rooms = retrieve_session_args(args)
            svc.update_session(session, date_time, event_id, is_playing, show_id, rooms)
        except Exception as e:
            return error_json(e), 400
        return success_json(f"Edited show {session.id}", svc.get_session_dict(session)), 201
        pass

    @staticmethod
    def delete(session_id=None):
        if not session_id:
            svc.reset_sessions()
        try:
            svc.delete_session(session_id)
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 403
        return None, 204
