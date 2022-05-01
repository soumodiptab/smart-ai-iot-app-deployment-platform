FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get -y install python-yaml

USER root

RUN pip3 install -r requirements.txt

RUN echo "export NODE_MANAGER_HOME=/app" >> ~/.bashrc

COPY . .

CMD . ~/.bashrc && python3 node_manager.py

#sudo docker run -d --name node-manager -p 5000:5000 node-manager
