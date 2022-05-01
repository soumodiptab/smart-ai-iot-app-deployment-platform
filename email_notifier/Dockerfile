# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "python3" ]
CMD ["email_processor.py"]


# # start by pulling the python image
# FROM python:3.8-alpine

# # copy the requirements file into the image
# COPY ./requirements.txt /app/requirements.txt

# # switch working directory
# WORKDIR /app

# RUN pip install --upgrade setuptools 

# # install the dependencies and packages in the requirements file
# RUN pip install -r requirements.txt

# # copy every content from the local file to the image
# COPY . /app

# # configure the container to run in an executed manner
# ENTRYPOINT [ "python3" ]
# CMD ["aiManager.py" ]
