import os

def create_requirements(path):
    os.system(f'pipreqs {path} --force')

create_requirements(os.getcwd())