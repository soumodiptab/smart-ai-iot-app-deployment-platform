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
COPY . .

#RUN useradd -r sudipta


#RUN apt-get -y install postfix
#RUN rm -rf /etc/localtime
#RUN ln -s /usr/share/zoneinfo/Asia/Calcutta /etc/localtime




# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#ENTRYPOINT [ "python3" ]
#CMD ["scheduler.py"]

CMD systemctl start cron && python3 scheduler.py
#ENTRYPOINT [ "python3" ]
#CMD ["scheduler.py"]

#sudo docker run -d --name <container_name> -e SCHEDULER_HOME="/app" -e APP_CRON_HOME="/app" <image_name>

