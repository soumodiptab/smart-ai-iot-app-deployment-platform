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


COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#ENTRYPOINT [ "python3" ]
#CMD ["deployer.py"]
CMD python3 deployer.py
