import datetime
import os.path
import bcrypt
import jwt
import markdown
from flask import Flask, request
from flask_restful import Api
from dotenv import load_dotenv

import data.mongo_setup as mongo_setup
from exceptions.exceptions import NotFoundError, AuthenticationError
from resources.show_resources import Show
from resources.session_resources import Session, success_json, error_json
from resources.user_resources import User
import services.login_service as login_svc

app = Flask(__name__)
api = Api(app)
load_dotenv()
mongo_setup.global_init()
secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    with open(os.getcwd() + "/README.md", "r") as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


@app.route("/login")
def login():
    def check_password_hash(pw, hashed):
        return bcrypt.checkpw(pw.encode("utf-8"), hashed)

    def auth_fail_msg():
        return error_json(AuthenticationError()), 401

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return auth_fail_msg()

    try:
        user = login_svc.find_user(username=auth.username)
        if check_password_hash(auth.password, user.password):
            token = jwt.encode({
                "publicId": str(user.publicId),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, secret_key)
            return success_json("Login success", {"token": token})
        return auth_fail_msg()
    except NotFoundError:
        return auth_fail_msg()


api.add_resource(Show, "/shows", "/shows/<string:show_id>")
api.add_resource(Session, "/sessions", "/sessions/<string:session_id>")
api.add_resource(User, "/users", "/users/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)

