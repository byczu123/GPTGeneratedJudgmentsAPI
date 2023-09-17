from flask import Blueprint
import requests
from utils.html_parser import html_parser
from utils.constants import SAOS_API_URL

saos_api_blueprint = Blueprint("saos_api", __name__)


@saos_api_blueprint.route("/")
def index():
    text_context = get_justification()

    return text_context


def get_justification():
    url_to_fetch = requests.get(SAOS_API_URL).json()["items"][0].get("href")
    text_context = html_parser(requests.get(url_to_fetch).json()["data"].get("textContent"))

    return text_context
