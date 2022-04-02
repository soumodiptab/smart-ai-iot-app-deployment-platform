import json
import zipfile
import os
import hashlib
from jsonschema import Draft7Validator
from kafka import KafkaProducer


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


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


def get_file_name(file_path):
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]


def validate_object(obj, schema):
    validator = Draft7Validator(schema)
    validation_errors = sorted(
        validator.iter_errors(obj), key=lambda e: e.path)

    errors = []

    for error in validation_errors:
        message = error.message
        if error.path:
            message = "[{}] {}".format(
                ".".join(str(x) for x in error.absolute_path), message
            )

        errors.append(message)
    return errors


def send_message(topic_name, message):
    producer = KafkaProducer(bootstrap_servers=[
        'localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic_name, message)


def allowed_file_extension(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
