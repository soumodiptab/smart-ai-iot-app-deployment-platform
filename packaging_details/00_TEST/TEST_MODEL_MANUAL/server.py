from flask import Flask, request, jsonify

import sys

from tensorflow import keras

from uuid import uuid4
import json
import os

from preprocess import preprocess
from postprocess import postprocess
portId = 4901

app = Flask(__name__)


@app.route('/predict/<modelId>', methods=['POST'])
def predict(modelId):
    data = request.files['image'].read()
    img_name = uuid4().hex+'.jpg'
    decodeit = open(f'{img_name}', 'wb')
    decodeit.write(data)
    decodeit.close()
    preprocessed = preprocess(img_name)
    os.remove(f'{img_name}')
    filename = 'model.h5'
    loaded_model = keras.models.load_model(filename)
    pred = loaded_model.predict(preprocessed)
    out = postprocess(pred)
    output = {'output': out}
    return jsonify(output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4901, debug=False)
