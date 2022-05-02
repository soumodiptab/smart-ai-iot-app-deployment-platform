from datetime import date
from kafka import KafkaConsumer
import json
import time
from utils import json_config_loader
import os
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
consumer = KafkaConsumer('logging', group_id='g',
                         bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
print(' Initializing logger....')
time.sleep(2)
print(' [LOGGER INITIALIZED...]')
try:
    for message in consumer:
        current_date = date.today()
        LOG_FILE = str(current_date)+"_platform.log"
        log_message = message.value
        PATH = os.path.join("logs", LOG_FILE)
        with open(PATH, 'a') as file_handle:
            # level timestamp sysname messsage
            
            file_handle.write(
                "{}\t[{}]\t[{}]\t\t\t{}\n".format(
                    log_message['timestamp'],
                    log_message['level'],
                    # log_message['ip'],
                    log_message['sys_name'],
                    log_message['info']
                )
            )
except:
    print('Exiting...')
finally:
    consumer.commit()
    consumer.close()
