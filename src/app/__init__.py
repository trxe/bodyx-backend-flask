import datetime
import json
import os.path
import time

import bcrypt
import jwt
import markdown
from flask import Flask, request, Response
from flask_restful import Api
from dotenv import load_dotenv
from pathlib import Path
from flask_cors import CORS


import data.mongo_setup as mongo_setup
from exceptions.exceptions import NotFoundError, AuthenticationError
from resources.show_resources import Show
from resources.session_resources import Session, success_json, error_json
from resources.user_resources import User
from resources.running_info_resources import RunningInfo
from resources.sse_resources import ServerSentEvents, format_sse
import services.login_service as login_svc

app = Flask(__name__)
api = Api(app)
load_dotenv()
CORS(app)
mongo_setup.global_init()
secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    with open(Path(os.getcwd()) / "README.md", "r") as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


@app.route("/login")
def login():
    def check_password_hash(pw, hashed):
        return bcrypt.checkpw(pw.encode("utf-8"), hashed)

    def auth_fail_msg(msg=None):
        return error_json(AuthenticationError(msg)), 401

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return auth_fail_msg()
    if not auth:
        return auth_fail_msg("No username and password")
    elif not auth.username:
        return auth_fail_msg("No username")
    elif not auth.password:
        return auth_fail_msg("No password")

    try:
        user = login_svc.find_user(username=auth.username)
        if check_password_hash(auth.password, user.password):
            token = jwt.encode({
                "publicId": str(user.publicId),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=480)
            }, secret_key)
            return success_json("Login success", {"token": token, "isAdmin": user.isAdmin})
        return auth_fail_msg("Wrong password")
    except NotFoundError:
        return auth_fail_msg("Username not found")


@app.route("/heartbeat")
def heartbeat():
    def pacemaker():
        while True:
            yield format_sse(json.dumps({}), event="heartbeat")
            time.sleep(1.0)
    return Response(pacemaker(), mimetype="text/event-stream")

'''
@app.route("/listen")
def listen():
    def respond_to_client():
        msgs = announcer.listen()
        while True:
            # blocks until new message arrives
            msg = msgs.get()
            print("sending running info...", msg)
            data = svc.get_running_info_dict(svc.get_running_info())
            yield format_sse(json.dumps(data), event="runningInfo")
    return Response(respond_to_client(), mimetype="text/event-stream")


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\ndata: {data}\n\n'
    return msg
'''


api.add_resource(Show, "/shows", "/shows/<string:show_id>")
api.add_resource(Session, "/sessions", "/sessions/<string:session_id>")
api.add_resource(User, "/users", "/users/<string:user_id>")
api.add_resource(RunningInfo, "/runningInfo")
api.add_resource(ServerSentEvents, "/online/<string:token>")

if __name__ == "__main__":
    app.run(debug=True)

