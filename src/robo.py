from flask import request, jsonify
from server import app
import os

def save_file(file):
    
    file_name = file.split('/')
    file_name = file[-1]

    ext = file_name.split('.')
    ext = ext[-1]

    if (ext not in app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'message': 'O arquivo não pode ser salvo, pois não tem o formato permitido'})
    else:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        print('O arquivo foi salvo com sucesso')

def process():
    data = request.get_json()
    
    save_file(data['file'])
    
    return jsonify([1, 2, 3])