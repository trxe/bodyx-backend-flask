import os.path
import markdown
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

import data.mongo_setup as mongo_setup
from resources.show_resources import Show

app = Flask(__name__)
api = Api(app)
load_dotenv()
mongo_setup.global_init()


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + "/README.md", "r") as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


api.add_resource(Show, "/shows", "/shows/<int:show_id>")

if __name__ == "__main__":
    app.run(debug=True)

