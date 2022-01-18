import datetime
import json
import os.path
import time

import bcrypt
import jwt
import markdown
from flask import Flask, request
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
from resources.sse_resources import ServerSentEvents
import services.login_service as login_svc

from gevent import monkey
monkey.patch_all()

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
        if user.isLoggedIn:
            return auth_fail_msg(f"{user.username} is already logged in on another device/tab." +
                                 "Contact your administrator if you think this is a mistake.")
        if check_password_hash(auth.password, user.password):
            token = jwt.encode({
                "publicId": str(user.publicId),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=480)
            }, secret_key)
            login_svc.set_login_user(user, is_logged_in=True)
            return success_json("Login success", {"token": token, "isAdmin": user.isAdmin})
        return auth_fail_msg("Wrong password")
    except NotFoundError:
        return auth_fail_msg("Username not found")


@app.route("/logout", methods=["POST"])
def logout():
    try:
        user_info = request.get_json()
        user = login_svc.find_user(username=user_info.get("username"))
        login_svc.set_login_user(user, False)
        return success_json("Logout success", {})
    except NotFoundError:
        return error_json(Exception("Username not found"))


api.add_resource(Show, "/shows", "/shows/<string:show_id>")
api.add_resource(Session, "/sessions", "/sessions/<string:session_id>")
api.add_resource(User, "/users", "/users/<string:user_id>")
api.add_resource(RunningInfo, "/runningInfo")
api.add_resource(ServerSentEvents, "/online/<string:token>")

if __name__ == "__main__":
    app.run(debug=True)

