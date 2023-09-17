from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from api.saos import saos_api_blueprint
from api.gpt import gpt_api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:root@localhost/gjja'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.register_blueprint(saos_api_blueprint, url_prefix='/saos')
app.register_blueprint(gpt_api_blueprint, url_prefix='/gpt')

if __name__ == '__main__':
    app.run()
