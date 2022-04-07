from os import rmdir
import docker
from git import Repo
import json
import shutil
REPO_FOLDER = 'deployment'


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data


print('[info]: Deleting previous deployment repository')
shutil.rmtree(REPO_FOLDER)
credentials = json_config_loader('git_credentials.json')
username = credentials['user_name']
password = credentials['password']
print('[info]: Downloading deployment package...')
remote = f"https://{username}:{password}@github.com/soumodiptab/smart-ai-iot-app-deployment-platform.git"
Repo.clone_from(remote, REPO_FOLDER)
print('[info]: Deployment package downloaded...')

