#FROM python:3.8-slim-buster

FROM ubuntu:20.04

WORKDIR /app

COPY requirements.txt requirements.txt
#COPY ..
RUN apt-get update -y
RUN apt upgrade -y
RUN apt-get -y install cron
RUN apt-get -y install systemctl
RUN systemctl start cron
RUN apt install -y postfix

RUN apt-get install python3.8 -y
RUN apt-get install python3-pip python-dev -y

USER root

RUN mkfifo /var/spool/postfix/public/pickup
RUN service postfix restart
RUN touch /var/mail/root

RUN pip3 install -r requirements.txt

RUN echo "export SCHEDULER_HOME=/app" >> ~/.bashrc
RUN echo "export APP_CRON_HOME=/app" >> ~/.bashrc

COPY . .

ENV TZ Asia/Calcutta
CMD . ~/.bashrc && echo 'Asia/Calcutta' >/etc/timezone && dpkg-reconfigure -f noninteractive tzdata && systemctl start postfix && systemctl start cron && python3 scheduler.py

#sudo docker run -d --name <container_name> <image_name>

