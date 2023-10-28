from flask import request, jsonify, Blueprint

# from app import db

user_api_blueprint = Blueprint("user", __name__)


@user_api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data['email'] == "test":
        return jsonify({'message': 'Registration successful'})

    # if 'email' not in data or 'password' not in data:
    #     return jsonify({'error': 'Missing email or password'}), 400
    #
    # email = data['email']
    # password = data['password']
    #
    # existing_user = User.query.filter_by(email=email).first()
    #
    # if existing_user:
    #     return jsonify({'error': 'Email already registered'}), 400
    #
    # new_user = User(email=email,password=password)
    # db.session.add(new_user)
    # db.session.commit()

    return jsonify({'message': 'Registration successful112'})
