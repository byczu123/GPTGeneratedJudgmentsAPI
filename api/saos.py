from flask import Blueprint
import requests
from utils.html_parser import html_parser
from utils.constants import SAOS_API_URL

saos_api_blueprint = Blueprint("saos", __name__)


@saos_api_blueprint.route("/")
def index():

    return get_justification()


def get_justification():
    url_to_fetch = requests.get(SAOS_API_URL).json()["items"][0].get("href")

    return html_parser(requests.get(url_to_fetch).json()["data"].get("textContent"))
