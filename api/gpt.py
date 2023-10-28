import openai
import requests
from flask import Blueprint, jsonify, request
from utils.constants import SAOS_API_URL, OPEN_AI_KEY
from utils.html_parser import html_parser

gpt_api_blueprint = Blueprint("gpt", __name__)

openai.api_key = OPEN_AI_KEY


@gpt_api_blueprint.route("/fetch", methods=['POST'])
def index():
    query_params = request.get_json()
    return jsonify({'status': 'ok'})

    # response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "You
    # are a legal advisor tasked with writing a legal opinion or reasoning " "for a court case."}, {"role": "user",
    # "content": "Please draft the beginning of reasoning for the court's decision in the case " "of Smith v.
    # Johnson. "}, ] )
    #
    # return response


def build_url(query_params):
    legal_base = query_params.get('legal_base', '')
    referenced_regulation = query_params.get('referenced_regulation', '')
    judge_name = query_params.get('judge_name', '')
    case_number = query_params.get('case_number', '')
    court_type = query_params.get('court_type', '')
    court_name = query_params.get('court_name', '')
    chamber_name = query_params.get('chamber_name', '')
    keywords = query_params.get('keywords', '')
    judgment_date_from = query_params.get('judgment_date_from', '')
    judgment_date_to = query_params.get('judgment_date_to', '')

    saos_url = (SAOS_API_URL + f"&legalBase={legal_base}"
                               f"&referencedRegulation={referenced_regulation}"
                               f"&judgeName={judge_name}&caseNumber={case_number}"
                               f"&ccCourtType={court_type}"
                               f"&ccCourtName={court_name}"
                               f"&scChamberName={chamber_name}"
                               f"&judgmentTypes=REASONS"
                               f"&keywords={keywords}&judgmentDateFrom={judgment_date_from}"
                               f"&judgmentDateTo={judgment_date_to}")

    return get_justification(saos_url)


def get_justification(saos_url):
    url_to_fetch = requests.get(saos_url).json()["items"][0].get("href")

    return jsonify(html_parser(requests.get(url_to_fetch).json()["data"].get("textContent")))
