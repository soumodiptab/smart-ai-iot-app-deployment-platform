#FROM python:3.8-slim-buster

FROM ubuntu:20.04

WORKDIR .

COPY requirements.txt requirements.txt
#COPY ..
RUN apt-get update -y
RUN apt upgrade -y
RUN apt-get -y install cron	
RUN apt install -y postfix

RUN pip3 install -r requirements.txt

RUN useradd -r sudipta
USER sudipta

#RUN apt-get -y install postfix
#RUN rm -rf /etc/localtime
#RUN ln -s /usr/share/zoneinfo/Asia/Calcutta /etc/localtime

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "python3" ]
CMD ["scheduler.py"]
