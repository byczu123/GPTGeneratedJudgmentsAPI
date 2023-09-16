from flask import Blueprint

gpt_api_blueprint = Blueprint("gpt_api", __name__)


@gpt_api_blueprint.route("/")
def index():
    return "This is gpt api blueprint"
