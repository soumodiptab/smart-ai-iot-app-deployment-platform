import json
from re import L
import sys
from zipfile import ZipFile

def generateDockerFile(path):
    extract_path=" "
    with ZipFile(path, 'r') as zip:
        path = path[:-4]
        print(path)
        zip.extractall(path)
    
    print(path)
    path1=path+"/config/control.json"
    f=open(path1)
    data=json.load(f)
    file_name=data['main']
    print(file_name)
    fname = path + '/Dockerfile'
    wdata = "FROM python:3.8-slim-buster\n\n"
    wdata += "WORKDIR /app\n\n"
    wdata += "COPY requirements.txt requirements.txt\n\n"
    wdata += "RUN pip3 install -r requirements.txt\n\n"
    wdata += "COPY . .\n\n"
    wdata += "ENTRYPOINT [ 'python3' ]\n\n"
    wdata += f'CMD ["{file_name}"]\n\n'
    with open(fname, 'w') as f:
        f.write('{}'.format(wdata))