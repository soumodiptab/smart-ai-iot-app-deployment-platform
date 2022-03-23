import json
import zipfile


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data


def open_zip_file(file_loc):
    zip_ref = zipfile.ZipFile(file_loc, 'r')
    zip_ref.extractall()
    zip_ref.close()


def pack_zip_file(folder_loc):
    pass


def delete_file(file_loc):
    pass


def allowed_file_extension(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
