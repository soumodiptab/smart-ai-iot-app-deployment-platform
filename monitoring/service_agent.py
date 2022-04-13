import pwd
import docker
import os
# os.chdir('../ai_manager')
# print(os.getcwd())
client = docker.from_env()


def show_containers():
    # displays all containers
    image_list = client.images.list()
    container_list = client.containers.list(True)
    pass


def get_stats(container_name):
    # need to decipher cpu / memory
    container = client.containers.get(container_name)
    status = container.stats(decode=None, stream=False)
    return status


def pull_repository():
    
    pass

def start_service(service):

    pass


def stop_service(service):
    #
    pass


def start():
    pass



stats = get_stats('kafka')
print(stats)
