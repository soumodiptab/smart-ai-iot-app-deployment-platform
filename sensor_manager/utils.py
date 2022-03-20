import json


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data
