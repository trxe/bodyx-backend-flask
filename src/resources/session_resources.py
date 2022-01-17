from flask import request
from flask_restful import Resource, inputs

import services.data_service as svc
from resources.response import error_json, success_json
from resources.user_resources import token_required
from exceptions.exceptions import NotFoundError, InvalidIdError, NoAccessError
from resources.message_announcer import announcer


def retrieve_session_args(args) -> tuple:
    date_time = None if not args.get("dateTime") else inputs.datetime_from_iso8601(args.get("dateTime"))
    event_id = args.get("eventId")
    show_id = args.get("showId")
    is_playing = args.get("isPlaying")
    rooms = args.get("rooms")
    return date_time, event_id, show_id, is_playing, rooms


class Session(Resource):
    @staticmethod
    @token_required
    def get(current_user, session_id=None):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        try:
            if session_id:
                session = svc.find_session_id(session_id)
                return success_json(f"found session with id {session_id}", svc.get_session_dict(session))
            elif request.args and "show_id" in request.args:
                show_id = request.args.get("show_id")
                sessions = svc.list_sessions_by_show(show_id)
                return success_json(f"Found sessions of show {show_id}:", list(map(svc.get_session_dict, sessions)))
            else:
                return success_json("Found sessions:", list(map(svc.get_session_dict, svc.list_sessions())))
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 400

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        try:
            args = request.json
            date_time, event_id, show_id, is_playing, rooms = retrieve_session_args(args)
            session = svc.create_session(date_time, event_id, show_id)
            announcer.announce("create show success")
            return success_json(f"Created new session {session.id}", svc.get_session_dict(session)), 201
        except Exception as e:
            return error_json(e), 400

    @staticmethod
    @token_required
    def put(current_user, session_id):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        try:
            session = svc.find_session_id(session_id)
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 400
        try:
            args = request.json
            date_time, event_id, show_id, is_playing, rooms = retrieve_session_args(args)
            svc.update_session(session, date_time, event_id, is_playing, show_id, rooms)
            announcer.announce("update show success")
        except Exception as e:
            return error_json(e), 400
        return success_json(f"Edited show {session.id}", svc.get_session_dict(session)), 201

    @staticmethod
    @token_required
    def delete(current_user, session_id=None):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        if not session_id:
            svc.reset_sessions()
        try:
            svc.delete_session(session_id)
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 400
        return None, 204
