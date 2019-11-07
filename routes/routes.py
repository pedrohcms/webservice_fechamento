from server import app
from flask import request
import importlib

robo = importlib.import_module('src.robo')

@app.route('/')
def index():
    return "Hello World"

@app.route('/postjson', methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    print(content['id'])
    print(content['name'])
    return 'JSON posted'

@app.route('/fechamento', methods=['GET'])
def fechamento():
    return robo.process()
