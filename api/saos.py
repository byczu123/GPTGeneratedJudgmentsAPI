import requests
from flask import Blueprint, jsonify, request

from utils.constants import SAOS_API_URL


saos_api_blueprint = Blueprint("saos", __name__)


@saos_api_blueprint.route("/")
def index():
    return get_justification()


@saos_api_blueprint.route("/params", methods=['POST'])
def get_params():
    if request.is_json:
        data = request.get_json()
        required_fields = [""]
        extracted_data = {}


        return




def get_justification(extracted_data):
    url_to_fetch = requests.get(SAOS_API_URL).json()["items"][0].get("href")

    return jsonify(requests.get(url_to_fetch).json()["data"].get("textContent"))
