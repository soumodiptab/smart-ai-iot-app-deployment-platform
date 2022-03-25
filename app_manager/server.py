
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from app_db_interaction import validate_app_and_insert, validate_app_instance
import json
import os
import shutil
from app_utils import process_application
from utils import allowed_file_extension
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
PORT = 8200

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


@app.route('/app/display', methods=['GET'])
def app_display():
    return jsonify({'status': '200'})


@app.route('/app/deploy/<app_id>', methods=['GET', 'POST'])
def app_dep_config():
    if request.method == "GET":
        return render_template('app_instance_config.html')
    else:
        app_config = request.get_json()
        if not validate_app_instance(app_config):
            process_application(app_config)
            flash('Application config successfully binded and stored.')
            return redirect(request.url)
        flash('Allowed file types are zip, rar')
        return redirect(request.url)


if __name__ == '__main__':
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
