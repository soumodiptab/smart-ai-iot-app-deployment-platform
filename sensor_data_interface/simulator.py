import logging
from kafka import KafkaConsumer
import json
import glob
from utils import json_config_loader
import sensor_data_interface.interfaces as interfaces
log = logging.getLogger('demo-logger')
sc_consumer = KafkaConsumer(
    "sensor_data_interface",
    group_id='simulator',
    bootstrap_servers=json_config_loader(
        'config/kafka.json')["bootstrap_servers"],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
global_directory = []

image_folders = glob.glob('images/*')
image_folder_count = len(image_folders)
current_image_folder = 0
device_settings = json_config_loader('config/sc_config.json')


def start_sc(sc):
    global current_image_folder
    device = sc["device"]
    type = sc["type"]
    ip_port = sc["ip_loc"]["ip"]+":"+sc["ip_loc"]["port"]
    try:
        if type not in device_settings.keys():
            expression = 'interfaces.'+type + \
                '('+'\"'+ip_port+'\")'
        else:
            latency = device_settings[type]['latency']
            expression = 'interfaces.'+type + \
                '('+'\"'+ip_port+'\"'+','+str(latency)+')'
        device = eval(expression)
    except:
        log.error('device not available')
        return
    if type == 'IMAGE':
        if image_folder_count == current_image_folder:
            current_image_folder = 0
        device.set_data_source(image_folders[current_image_folder])
        current_image_folder = current_image_folder + 1
    device.start()
    global_directory.append(device)


def stop_sc(sc):
    device = sc["device"]
    type = sc["type"]
    ip_port = sc["ip_loc"]
    geo_loc = sc["geo_loc"]

    try:
        for dev in global_directory:
            if dev.ip_port == ip_port:
                dev.stop()
    except:
        log.error('Device not present')


if __name__ == "__main__":
    for msg in sc_consumer:
        message_type = msg.value["message_type"]
        log.info(f"New sensor/controller request:{message_type}")
        if message_type == "SC_START":
            start_sc(msg.value)
        if message_type == "SC_STOP":
            stop_sc(msg.value)
        else:
            log.info("Un-registered message")
