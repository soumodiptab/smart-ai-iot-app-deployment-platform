from asyncio import tasks
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "secret key"


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    json_data = request.get_json()
    temp = json_data["temp"]
    pressure = json_data["pres"]
    return jsonify({"data": temp+pressure})


if __name__ == '__main__':
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
