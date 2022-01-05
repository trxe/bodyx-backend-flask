from flask_restful import Resource, reqparse

import services.data_service as svc

show_info_args = reqparse.RequestParser()
show_info_args.add_argument("enTitle", type=str, help="Enter a unique english title for this show.")
show_info_args.add_argument("cnTitle", type=str, help="Enter a chinese title for this show.")
show_info_args.add_argument("durationMins", type=int, help="Enter the duration (mins) of this show.")
show_info_args.add_argument("defaultRooms", type=list[dict], help="Enter default rooms of this show.")


class Show(Resource):
    @staticmethod
    def get(show_id=None):
        if show_id is not None:
            return svc.get_show_dict(svc.list_shows()[show_id])
        return list(map(svc.get_show_dict, svc.list_shows()))

    @staticmethod
    def post():
        args = show_info_args.parse_args()
        return {"show": args}, 201

    @staticmethod
    def put(show_id):
        args = show_info_args.parse_args()
        return {show_id: args}, 201

    @staticmethod
    def delete(show_id):
        return show_id, 204
