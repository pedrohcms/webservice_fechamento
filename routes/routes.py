from server import app
from flask import request, render_template
import importlib

robo = importlib.import_module('src.robo')

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/postjson', methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    print(content['id'])
    print(content['name'])
    return 'JSON posted'

@app.route('/fechamento', methods=['POST'])
def fechamento():
    return robo.process()