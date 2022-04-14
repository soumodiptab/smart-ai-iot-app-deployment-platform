FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
#COPY ..
RUN apt-get update
RUN apt-get -y install python-yaml
#RUN echo "export SCHEDULER_HOME=." > ~/.bashrc
#RUN source ~/.bashrc	

USER root
#RUN apt-get -y install cron

RUN pip3 install -r requirements.txt

#RUN useradd -r sudipta


COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "python3" ]
CMD ["node_manager.py"]
#sudo docker run -d --name node-manager -e NODE_MANAGER_HOME="/app"  -p 5000:5000 node-manager
