import requests
sample={'temp_max': 371, 'perc': 217}
json_out = requests.post(prediction_api, json=sample).json()