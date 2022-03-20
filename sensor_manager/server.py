from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
app = Flask(__name__)

UPLOAD_FOLDER = './temp/uploads/'


@app.route('/sc_type/upload', methods=['POST'])
def sc_type_upload():
    return jsonify({'prediction': values})


@app.route('/sc_instance/upload', methods=['POST'])
def sc_type_upload():
    return jsonify({'prediction': values})




if (__name__ == '__main__'):
    load_ai_files()
    app.run(port=8000, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
