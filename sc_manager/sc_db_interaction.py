
from logging import Logger
import logging
from utils import json_config_loader
from zipfile import ZipFile
log = logging.getLogger('demo-logger')


def validate_sc_type_and_insert(zip_file_loc):
    # first extract zip
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)


def insert_sc_record(sc_type):
    


def validator_sc_instance_and_insert(zip_file):
    pass
