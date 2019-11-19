from flask import Flask
import importlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object('config')

importlib.import_module('routes.routes')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)