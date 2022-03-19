import logging
from time import sleep
from platform_logger import get_logger
import logging
from faker import Faker
fake = Faker()
logger = get_logger('sensor_manager', 'localhost:9092')
while True:
    logger.info(fake.text())
    sleep(1)
