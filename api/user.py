from flask import request, jsonify, Blueprint
from flask_jwt_extended import unset_jwt_cookies, create_access_token

user_api_blueprint = Blueprint("user", __name__)


@user_api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data['email'] == "test":
        return jsonify({'message': 'Registration successful'})

    return jsonify({'message': 'Registration successful112'})


@user_api_blueprint.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)

    # Convert the bytes access_token to a string
    token_string = access_token.decode('utf-8')

    response = {"access_token": token_string}
    return response


@user_api_blueprint.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
