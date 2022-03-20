from platform import platform
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import json
import os
from utils import allowed_file_extension
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = './temp/uploads/'
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
        if file and allowed_file_extension(file.filename,ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are zip,rar')
            return redirect(request.url)


@app.route('/sc_instance/upload', methods=['POST', 'GET'])
def sc_instance_upload():
    return jsonify({'prediction': 'asd'})


if (__name__ == '__main__'):
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
