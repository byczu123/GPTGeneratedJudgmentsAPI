import os
import sqlite3

import openai
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from utils.constants import SAOS_API_URL, GPT_ENGINE_VALUE
from utils.gpt_constants import INTRODUCTION_PROMPT, MIDDLE_PART_PROMPT, FINISH_PART_PROMPT
from utils.html_parser import split_text, split_text_reverse, split_text_reverse1, parse_html
from utils.http_constants import JUSTIFICATION_FIELD, MESSAGE_FIELD, SUCCESSFUL_FEEDBACK_MESSAGE

gpt_api_blueprint = Blueprint("gpt", __name__)

gpt_engine = os.getenv(GPT_ENGINE_VALUE)

@jwt_required()
@gpt_api_blueprint.route("/query", methods=['POST'])
def query_page_route():
    query_params = request.get_json()
    justification_to_generate = query_params.get('justification_to_generate')

    saos_url = build_url(query_params)
    empowering_justification = parse_html(get_justification(saos_url))

    introduction_to_generate = generate_justification(INTRODUCTION_PROMPT, justification_to_generate,
                                                      split_text(empowering_justification))

    justification_parts = [introduction_to_generate]

    for i in range(3):
        if i == 0:
            justification_parts.append(
                generate_justification(MIDDLE_PART_PROMPT, justification_to_generate, introduction_to_generate))
        else:
            justification_parts.append(generate_justification(MIDDLE_PART_PROMPT, justification_to_generate,
                                                              split_text_reverse(justification_parts[i])))
    for i in range(3):
        if i == 0:
            justification_parts.append(generate_justification(FINISH_PART_PROMPT, justification_to_generate,
                                                              split_text_reverse(justification_parts[i + 2])))
        else:
            justification_parts.append(generate_justification(FINISH_PART_PROMPT,
                                                              justification_to_generate,
                                                              split_text_reverse1(justification_parts[i + 2])))

    final_justification = "\n\n".join(justification_parts)

    return jsonify({JUSTIFICATION_FIELD: final_justification})


@jwt_required()
@gpt_api_blueprint.route("/rate", methods=["POST"])
def rate_page_route():
    if request.method == "POST":
        data = request.get_json()

        justification = data.get('justification')
        feedback = data.get('feedback')
        rating = data.get('rating')
        user_id = 1

        insert_feedback(justification, feedback, rating, user_id)
        return jsonify({'status': 'success', MESSAGE_FIELD: SUCCESSFUL_FEEDBACK_MESSAGE}), 200

    return jsonify({'status': 'Failure', MESSAGE_FIELD: 'Error has occurred'}), 500


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

    return saos_url


def generate_justification(prompt, user_input, empowering_justification):
    formatted_prompt = prompt.format(user_input, empowering_justification)
    response = openai.Completion.create(
        engine=gpt_engine,
        prompt=formatted_prompt,
        max_tokens=3500,
        temperature=0.3
    )

    return response.choices[0].text


def get_justification(saos_url):
    url_to_fetch = requests.get(saos_url).json()["items"][0].get("href")

    return requests.get(url_to_fetch).json()["data"].get("textContent")


def insert_feedback(text, feedback, rating, user_id):
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO justification (text, feedback, rate, user_id) VALUES (?, ?, ?, ?)',
        (text, feedback, rating, user_id)
    )
    conn.commit()
    conn.close()
