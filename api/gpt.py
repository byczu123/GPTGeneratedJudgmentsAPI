import openai
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.html_parser import split_text, split_text_reverse, split_text_reverse1
import sqlite3
from utils.constants import SAOS_API_URL, OPEN_AI_KEY

gpt_api_blueprint = Blueprint("gpt", __name__)

openai.api_key = OPEN_AI_KEY


@jwt_required()
@gpt_api_blueprint.route("/fetch", methods=['POST'])
def index():
    query_params = request.get_json()
    justification_to_generate = query_params.get('justification_to_generate')

    saos_url = build_url(query_params)
    empowering_justification = get_justification(saos_url)

    introduction_to_generate = generate_justification_introduction(justification_to_generate,
                                                                   split_text(empowering_justification))

    justification_parts = [introduction_to_generate]

    for i in range(5):
        if i == 0:
            justification_parts.append(
                continue_generating_justification(justification_to_generate, introduction_to_generate))
        else:
            justification_parts.append(continue_generating_justification(justification_to_generate,
                                                                         split_text_reverse(justification_parts[i])))
    for i in range(3):
        if i == 0:
            justification_parts.append(finish_generating_justification(justification_to_generate, split_text_reverse(justification_parts[i+4])))
        else:
            justification_parts.append(continue_generating_justification(justification_to_generate, split_text_reverse1(justification_parts[i+4])))

    final_justification = "\n\n".join(justification_parts)

    return jsonify({'justification': final_justification})


@jwt_required()
@gpt_api_blueprint.route("/rate", methods=["POST"])
def rate():
    if request.method == "POST":
        data = request.get_json()

        justification = data.get('justification')
        feedback = data.get('feedback')
        rating = data.get('rating')
        user_id = 1

        insert_feedback(justification, feedback, rating, user_id)
        return jsonify({'status': 'success', 'message': 'Feedback submitted successfully'}), 200

    return jsonify({'status': 'Failure', 'message': 'Error has occured'}), 500


def insert_feedback(text, feedback, rating, user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO justification (text, feedback, rate, user_id) VALUES (?, ?, ?, ?)',
        (text, feedback, rating, user_id)
    )
    conn.commit()
    conn.close()


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


def get_justification(saos_url):
    url_to_fetch = requests.get(saos_url).json()["items"][0].get("href")

    return requests.get(url_to_fetch).json()["data"].get("textContent")


def generate_justification_introduction(user_input, empowering_justification):
    prompt = (f"Wygeneruj wstęp uzasadnienia wyroku sadowego w temacie: {user_input}, zachowujac strukture orzeczenia, "
              f"na podstawie fragmentu podanego uzasadnienia: {empowering_justification}")
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3500,
        temperature=0.3
    )

    return response.choices[0].text


def continue_generating_justification(user_input, justification_part):
    prompt = f"Kontynuuj generowanie uzasadnienia wyroku sadowego w temacie: {user_input}, zaczynając od: {justification_part}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3500,
        temperature=0.3
    )

    return response.choices[0].text


def finish_generating_justification(user_input, justification_part):
    prompt = (f"Kontynuuj generowanie uzasadnienia wyroku sadowego w temacie: {user_input}, zacznij od 'Sąd zważył co "
              f"następuje:' od: {justification_part}")
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3500,
        temperature=0.3
    )

    return response.choices[0].text
