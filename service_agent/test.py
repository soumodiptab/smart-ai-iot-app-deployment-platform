import docker
from elasticsearch import NotFoundError
client = docker.from_env()
try:
    container = client.containers.get('clever_moore')
    container.status
except:
    print('error')