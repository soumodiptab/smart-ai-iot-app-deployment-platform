FROM python:3.8-slim-buster

WORKDIR /app


COPY requirements.txt requirements.txt
#COPY ..
#RUN apt-get update
#RUN apt-get -y install python-yaml
#RUN echo "export SCHEDULER_HOME=." > ~/.bashrc
#RUN source ~/.bashrc	


#RUN apt-get -y install cron

USER root

RUN pip3 install -r requirements.txt

#RUN useradd -r sudipta

RUN echo "export DEPLOYER_HOME=/app" >> ~/.bashrc

COPY . .

CMD . ~/.bashrc && python3 deployer.py


#docker exec -it deployer bash
#sudo docker run -d --name deployer -p 5005:5005 deployer
