from flask import Response
from flask_restful import Resource
import json
import time

from resources.user_resources import user_lookup
from resources.response import error_json
from exceptions.exceptions import NotFoundError, InvalidTokenError
import services.data_service as svc


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\ndata: {data}\n\n'
    return msg


# Note: Currently just pinging every 5.0s due to heroku.
# https://devcenter.heroku.com/articles/request-timeout#long-polling-and-streaming-responses
class ServerSentEvents(Resource):
    @staticmethod
    def get(token: str):
        print("received token", token)
        try:
            user_lookup(token)
            print("check succeeded")

            def respond_to_client():
                while True:
                    print("sending running info...")
                    data = svc.get_running_info_dict(svc.get_running_info())
                    yield format_sse(json.dumps(data), event="runningInfo")
                    time.sleep(5.0)
            response = Response(respond_to_client(), mimetype="text/event-stream")
            response.headers["Access-Control-Allow-Origin"] = "*"
            print("response set up")
            return response
        except NotFoundError or InvalidTokenError:
            return error_json(InvalidTokenError()), 401
