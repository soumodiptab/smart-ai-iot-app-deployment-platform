
from ipaddress import ip_address
from flask import Flask, render_template, request, jsonify
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient
import logging
app = Flask(__name__)
app.secret_key = "secret key"
log = logging.getLogger('demo-logger')


@app.route('/', methods=['GET'])
def app_stat_config():
    return render_template('simple.html')


if __name__ == '__main__':
    app.run(port=6015, debug=True, use_debugger=False, host='0.0.0.0',
            use_reloader=False, passthrough_errors=True)
