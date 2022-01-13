import datetime
import os.path
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
import services.login_service as login_svc
import services.data_service as svc
from commands.message_announcer import MessageAnnouncer

app = Flask(__name__)
api = Api(app)
load_dotenv()
CORS(app)
mongo_setup.global_init()
secret_key = os.getenv("SECRET_KEY")

announcer = MessageAnnouncer()


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


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@app.route("/ping")
def ping():
    msg = format_sse(data='pong')
    announcer.announce(msg=msg)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


api.add_resource(Show, "/shows", "/shows/<string:show_id>")
api.add_resource(Session, "/sessions", "/sessions/<string:session_id>")
api.add_resource(User, "/users", "/users/<string:user_id>")
api.add_resource(RunningInfo, "/runningInfo")

if __name__ == "__main__":
    app.run(debug=True)

