from flask import request, jsonify, Blueprint
from flask_jwt_extended import unset_jwt_cookies, create_access_token, decode_token
import sqlite3
from jwt.exceptions import ExpiredSignatureError
from utils.http_constants import MESSAGE_FIELD, INVALID_CREDENTIALS_MESSAGE, ACCESS_TOKEN_FIELD, AUTHORIZATION_HEADER, \
    BEARER_FIELD, SUCCESSFUL_LOGOUT_MESSAGE, VALID_FIELD, EXPIRED_TOKEN_MESSAGE, TOKEN_NOT_PROVIDED_MESSAGE, \
    METHOD_NOT_ALLOWED_MESSAGE

user_api_blueprint = Blueprint("user", __name__)


@user_api_blueprint.route('/token', methods=["POST"])
def create_token_route():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = query_user(email, password)

        if user:
            return {ACCESS_TOKEN_FIELD: create_access_token(identity=email)}

        else:
            return {MESSAGE_FIELD: INVALID_CREDENTIALS_MESSAGE}, 401
    else:
        return jsonify({MESSAGE_FIELD: METHOD_NOT_ALLOWED_MESSAGE}), 405


@user_api_blueprint.route('/validate-token', methods=['POST'])
def validate_token_route():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER)

    if authorization_header and authorization_header.startswith(BEARER_FIELD):
        token = authorization_header.split(' ')[1]

        try:
            decoded_token = decode_token(token)
            return jsonify({VALID_FIELD: True, MESSAGE_FIELD: decoded_token['sub']}), 200

        except Exception as e:
            return jsonify({VALID_FIELD: False, MESSAGE_FIELD: str(e)}), 401

        except ExpiredSignatureError:
            return jsonify({VALID_FIELD: False, MESSAGE_FIELD: EXPIRED_TOKEN_MESSAGE}), 401

    else:
        return jsonify({MESSAGE_FIELD: TOKEN_NOT_PROVIDED_MESSAGE}), 400


@user_api_blueprint.route("/logout", methods=["POST"])
def logout():
    response = jsonify({MESSAGE_FIELD: SUCCESSFUL_LOGOUT_MESSAGE})
    unset_jwt_cookies(response)
    return response, 200


def query_user(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    conn.close()

    return user
