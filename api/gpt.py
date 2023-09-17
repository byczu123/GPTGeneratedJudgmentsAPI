from flask import Blueprint, jsonify
import requests

gpt_api_blueprint = Blueprint("gpt", __name__)

url = 'http://127.0.0.1:5000/saos/'


@gpt_api_blueprint.route("/")
def index():
    response = requests.get(url)
    return jsonify({"text": response.text})
