import json


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data


def json_config_saver(data, config_file_loc):
    fstream = open(config_file_loc, "w")
    json_repr = json.dumps(data)
    fstream.write(json_repr)
    fstream.close()


config_map = {
    1: "dev",
    2: "staging",
    3: "prod",
}

print(' Change config files to : ')
print('1. dev\n2. staging\n3. prod\n4. Exit')
choice = int(input('Enter choice\n'))
if choice == 4:
    exit(0)
modules = (
    "sc_data_interface",
    "ai_manager",
    "monitoring",
    "app_manager",
    "sc_manager",
    "request_manager",
    "api_layer",
    "logging",
    "email_notifier"
)
print('Select:\n1. all\n2. Select module:')
for i in modules:
    print(i)
print('-----------------------------------------')
module_selection = input()
if not (module_selection in modules or module_selection == 'all'):
    print('error')
    exit(0)
environment_folder = "env/"+config_map[choice]
kafka_config = json_config_loader(environment_folder+"/kafka.json")
db_config = json_config_loader(environment_folder+"/db.json")
if module_selection == 'all':
    for module in modules:
        config_folder = "../{}/config".format(module)
        json_config_saver(kafka_config, config_folder+"/kafka.json")
        json_config_saver(db_config, config_folder+"/db.json")
else:
    config_folder = "../{}/config".format(module_selection)
    json_config_saver(kafka_config, config_folder+"/kafka.json")
    json_config_saver(db_config, config_folder+"/db.json")
