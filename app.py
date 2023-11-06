from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from api.saos import saos_api_blueprint
from api.gpt import gpt_api_blueprint
from api.user import user_api_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:root@localhost/gjja'
app.config["JWT_SECRET_KEY"] = "some-secret-key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)


CORS(app)

jwt = JWTManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.register_blueprint(saos_api_blueprint, url_prefix='/saos')
app.register_blueprint(gpt_api_blueprint, url_prefix='/gpt')
app.register_blueprint(user_api_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run()
