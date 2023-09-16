from flask import Flask
from saos_api.routes import saos_api_blueprint
from gpt_api.routes import gpt_api_blueprint

app = Flask(__name__)

app.register_blueprint(saos_api_blueprint, url_prefix='/saos_api')
app.register_blueprint(gpt_api_blueprint, url_prefix='/gpt_api')

if __name__ == '__main__':
    app.run(debug=True)
