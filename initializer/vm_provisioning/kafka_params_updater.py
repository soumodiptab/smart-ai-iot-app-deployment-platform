import sys

VM_IP = sys.argv[1]

lines = []
with open("kafka_2.13-3.1.0/config/server.properties", "r") as server_properties_file:
    lines = server_properties_file.readlines()

with open("kafka_2.13-3.1.0/config/server.properties", "w") as updated_server_properties_file:
    for line in lines:
        if line.startswith("#advertised.listeners") :
            line = line.replace("your.host.name", VM_IP)
            line = line.replace("#", "")
        updated_server_properties_file.write(line)