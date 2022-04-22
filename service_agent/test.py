import os
import docker


def docker_trial():
    client = docker.from_env()
    try:
        container = client.containers.get('clever_moore')
        container.status
    except:
        print('error')

def environ_test():
    os.environ.get('REPO_LOCATION')
    