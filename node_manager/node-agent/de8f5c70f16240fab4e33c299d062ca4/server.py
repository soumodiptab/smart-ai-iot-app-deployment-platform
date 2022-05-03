from flask import Flask, request, jsonify

import sys

import pickle

import json
import os

from preprocess import preprocess
from postprocess import postprocess
portId = sys.argv[1]

app = Flask(__name__)

@app.route('/predict/<modelId>', methods=['POST'])

def predict(modelId):
	data = request.json
	preprocessed = preprocess(data)
	filename = 'model.pkl'
	loaded_model = pickle.load(open(filename, 'rb'))
	pred = loaded_model.predict(preprocessed)
	out=postprocess(pred)
	output = {'output': out}
	return jsonify(output)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = portId, debug = False)
