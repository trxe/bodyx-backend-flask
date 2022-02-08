from flask import request
from flask_restful import Resource

import services.data_service as svc
from resources.response import error_json, success_json
from resources.user_resources import token_required
from exceptions.exceptions import NotFoundError, InvalidIdError, NoAccessError
# from resources.message_announcer import announcer


def retrieve_running_info_args(args) -> tuple:
    show_id = args.get("showId")
    session_id = args.get("sessionId")
    is_house_open = args.get("isHouseOpen")
    return show_id, session_id, is_house_open


class RunningInfo(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        if not current_user:
            return error_json(NoAccessError()), 401

        running_info = svc.get_running_info()
        print(running_info.showId, running_info.sessionId, running_info.isHouseOpen)
        running_info_dict = svc.get_running_info_dict(running_info)
        return success_json("Currently showing", running_info_dict)

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        try:
            args = request.json
            show_id, session_id, is_house_open = retrieve_running_info_args(args)
            running_info = svc.update_running_info(show_id, session_id, is_house_open)
            announcer.announce("start show success")
            return success_json(f"Now running show {show_id}, session {session_id}",
                                svc.get_running_info_dict(running_info))
        except NotFoundError as e:
            return error_json(e), 404
        except InvalidIdError as e:
            return error_json(e), 400

    @staticmethod
    @token_required
    def delete(current_user):
        if not current_user.isAdmin:
            return error_json(NoAccessError()), 401

        svc.reset_running_info()
        # announcer.announce("end show success")
        return success_json("Deleted", data=None), 204
