
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from app_db_interaction import validate_app_and_insert, validate_app_instance
import json
import os
import shutil
from logging import Logger
import logging
from pymongo import MongoClient
from app_utils import process_application
from utils import allowed_file_extension
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
PORT = 8200
log = logging.getLogger('demo-logger')
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/app/upload', methods=['POST', 'GET'])
def app_type_upload():
    if request.method == "GET":
        return render_template('app_upload.html')
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
            if validate_app_and_insert(relative_file_path):
                flash('Zip File successfully uploaded')
            else:
                flash('Zip File is not correct')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar')
            return redirect(request.url)


@app.route('/app/display', methods=['GET', 'POST'])
def app_display():
    if request.method == 'POST':
        appid_form = request.form.get('appid')
        return redirect(url_for('app_dep_config', appid=appid_form))
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        app_records = client.app_db.app
        app_list = []
        for app_record in app_records.find():
            display_record = {
                "app_id": app_record["app_id"],
                "app_name": app_record["app_name"],
                "description": app_record["description"],
                "scripts": app_record["scripts"],
                "controller": app_record["controller"],
                "sensor": app_record["sensor"],
                "model": app_record["model"],
                "database": app_record["database"],
                "sensors": app_record["sensors"],
                "controllers": app_record["controllers"],
                "models": app_record["models"]

            }
            app_list.append(display_record)
            log.info(app_list)
        return render_template('display.html', tasks=app_list)
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


@app.route('/app/deploy/<appid>', methods=['GET', 'POST'])
def app_dep_config(appid):
    if request.method == "GET":
        return render_template('scheduling_form.html', app_id=appid)
    else:
        app_config = request.get_json()
        if validate_app_instance(app_config):
            process_application(app_config)
            flash('Application config successfully binded and stored.')
            return redirect()
        else:
            flash('placeholder')
        return render_template('')


if __name__ == '__main__':
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
