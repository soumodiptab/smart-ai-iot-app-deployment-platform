from platform import platform
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from sc_db_interaction import validate_sc_type_and_insert
import json
import os
import pymongo
import shutil
from utils import allowed_file_extension
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
MONGO_DB_URL = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_DB_URL)
sc_db = client["sc_db"]
sc_type = sc_db["sc_type"]
sc_instance = sc_db["sc_instance"]
sc_app_map = sc_db["sc_app_map"]
sc_appinstance_map = sc_db["sc_app_instance_map"]
PORT = 8100

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/sc_type/upload', methods=['POST', 'GET'])
def sc_type_upload():
    if request.method == "GET":
        return render_template('sc_type_upload.html')
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file_extension(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            relative_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(relative_file_path)
            if validate_sc_type_and_insert(relative_file_path):
                flash('Zip File successfully uploaded')
            else:
                flash('Zip File is not correct')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar')
            return redirect(request.url)


@app.route('/sc_instance/upload', methods=['POST', 'GET'])
def sc_instance_upload():

    return jsonify({'status': '200'})


@app.route('/sc_type/display', methods=['POST', 'GET'])
def sc_type_display():
    return jsonify({'status': '200'})


if __name__ == '__main__':
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
