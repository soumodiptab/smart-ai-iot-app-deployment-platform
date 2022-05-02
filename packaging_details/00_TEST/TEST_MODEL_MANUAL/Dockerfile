FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY requirementsDS.txt requirementsDS.txt

RUN pip3 install -r requirementsDS.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD ["server.py", "6015"]

