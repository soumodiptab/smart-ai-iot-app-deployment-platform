from flask import Flask, request, jsonify

import sys

import pickle

import json

from preprocess import preprocess
from postprocess import postprocess
portId = sys.argv[1]

app = Flask(__name__)

@app.route('/predict/<modelId>', methods=['POST'])

def predict(modelId):
	data = request.json
	perc = data['perc']
	temp_max = data['temp_max']
	l = [perc,temp_max]
	preprocessed = preprocess(l)
	filename = 'model.pkl'
	loaded_model = pickle.load(open(filename, 'rb'))
	pred = loaded_model.predict(preprocessed)
	out=postprocess(pred)
	output = {'output': out}
	return jsonify(output)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = portId, debug = False)
