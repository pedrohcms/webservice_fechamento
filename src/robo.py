from flask import request, jsonify
from server import app
import os

def save_file(file):
    
    file_name = file.split('\\')
    file_name = file_name[-1]
    
    ext = file_name.split('.')
    ext = ext[-1]
    
    if (ext not in app.config['ALLOWED_EXTENSIONS']):
        print('O arquivo não pode ser salvo, pois não tem o formato permitido')
    else:
        if os.path.exists('C:\\file'):
            print('Diretorio C:\\file existe')
        else:
            os.mkdir('C:\\file')
        print('O arquivo foi salvo com sucesso')

def process():
    data = request.get_json()

    save_file(data['file'])
    
    return jsonify([1, 2, 3])
