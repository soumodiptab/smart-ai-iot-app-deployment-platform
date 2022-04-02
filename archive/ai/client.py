import requests
import json
while True:
    url = 'http://localhost:6001/getModelInfo'

    modelId = requests.get(url).content.decode("utf-8")

    modelId = json.loads(modelId)["modelId"]


    url = 'http://localhost:6001/predict/' + str(modelId) 

    perc = 10.9
    temp_max = 10.6

    #output --> rain

    data = {"perc": perc, "temp_max": temp_max}

    response = requests.post(url, json=data)

    # d = {0:"Drizzle", 1:"Fog", 2:"Rain", 3:"Snow", 4:"Sun"}

    # res = int(response.content.decode("utf-8"))

    # print("Output:", d[res])

    res = response.content.decode("utf-8")
    print("Output: " + res)