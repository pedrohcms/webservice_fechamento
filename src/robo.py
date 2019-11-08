from flask import request, jsonify
from server import app
import os

def save_file(file):
    
    ext = file.filename.split('.')
    ext = ext[-1]
    
    if (ext not in app.config['ALLOWED_EXTENSIONS']):
        print('O arquivo não pode ser salvo, pois não tem o formato permitido')
    else:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        print('O arquivo foi salvo com sucesso')

def process():

    save_file(request.files['file'])
    
    return jsonify([1, 2, 3])
