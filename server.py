from flask import Flask
import importlib

app = Flask(__name__)

app.config.from_object('config')

importlib.import_module('routes.routes')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)