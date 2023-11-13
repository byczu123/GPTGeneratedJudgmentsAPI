from flask import request, jsonify, Blueprint
from flask_jwt_extended import unset_jwt_cookies, create_access_token, decode_token
import sqlite3

from jwt import ExpiredSignatureError

user_api_blueprint = Blueprint("user", __name__)


@user_api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data['email'] == "test":
        return jsonify({'message': 'Registration successful'})

    return jsonify({'message': 'Registration successful112'})


@user_api_blueprint.route('/token', methods=["POST"])
def create_token():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = query_user(email, password)

        if user:
            access_token = create_access_token(identity=email)
            token_string = access_token.decode('utf-8')
            return {"access_token": token_string}

        else:
            return {"msg": "Wrong email or password"}, 401


@user_api_blueprint.route('/validate-token', methods=['POST'])
def validate_token_route():
    authorization_header = request.headers.get('Authorization')

    if authorization_header and authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ')[1]

        try:
            decoded_token = decode_token(token)

            return jsonify({"valid": True, "identity": decoded_token['sub']}), 200
        except Exception as e:
            return jsonify({"valid": False, "error": str(e)}), 401
        except ExpiredSignatureError:
            return jsonify({"valid": False, "msg": "Token has expired"}), 401
    else:
        return jsonify({"msg": "Token not provided"}), 400


@user_api_blueprint.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


def query_user(email, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()

        return user


def validate_token(token):
    try:
        # Decode the token to check its validity
        decoded_token = decode_token(token)

        # If the decoding is successful, the token is valid
        return {"valid": True, "identity": decoded_token['identity']}
    except Exception as e:
        # If decoding fails, the token is invalid
        return {"valid": False, "error": str(e)}
