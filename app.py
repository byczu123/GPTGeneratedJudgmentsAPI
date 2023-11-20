import os
from datetime import timedelta

import openai
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.gpt import gpt_api_blueprint
from api.user import user_api_blueprint
from utils.constants import OPEN_AI_KEY_VALUE, JWT_SECRET_KEY_VALUE, GPT_ENGINE_VALUE, SECRET_KEY_VALUE

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(SECRET_KEY_VALUE)
app.config['JWT_SECRET_KEY'] = os.getenv(JWT_SECRET_KEY_VALUE)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

openai.api_key = os.getenv(OPEN_AI_KEY_VALUE)

CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(gpt_api_blueprint, url_prefix='/gpt')
app.register_blueprint(user_api_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)