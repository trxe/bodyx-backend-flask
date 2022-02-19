from flask import Response
from flask_restful import Resource
import json
import time

from resources.user_resources import user_lookup
from resources.response import error_json
from exceptions.exceptions import NotFoundError, InvalidTokenError
import services.data_service as svc
from resources.message_announcer import announcer


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\ndata: {data}\n\n'
    return msg


# https://devcenter.heroku.com/articles/request-timeout#long-polling-and-streaming-responses
class ServerSentEvents(Resource):
    @staticmethod
    def get(token: str):
        print("received token", token)
        try:
            if not token or token == "null":
                return Response(None)
            user_lookup(token)
            print("check succeeded")

            def respond_to_client():
                msgs = announcer.listen()
                while True:
                    # blocks until new message arrives
                    msg = msgs.get()
                    print("sending running info...", msg)
                    data = svc.get_running_info_dict(svc.get_running_info())
                    yield format_sse(json.dumps(data), event="runningInfo")

            response = Response(respond_to_client(), mimetype="text/event-stream")
            response.headers["Access-Control-Allow-Origin"] = "*"
            print("response set up")
            return response
        except NotFoundError or InvalidTokenError:
            return error_json(InvalidTokenError()), 401
