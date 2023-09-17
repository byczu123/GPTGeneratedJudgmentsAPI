from flask import Blueprint
import requests

gpt_api_blueprint = Blueprint("gpt_api", __name__)

url = 'http://localhost:5000/saos_api/'


@gpt_api_blueprint.route("/")
def index():
    response = requests.get(url).json()
    return response
