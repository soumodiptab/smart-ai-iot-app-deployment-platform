import pymongo
MONGO = "mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(MONGO)

databases = myclient.list_database_names()

rm_database = ['admin', 'config', 'local',
               'ip_db', 'node_manager_db', 'initialiser_db']
databases_final = [
    db_name for db_name in databases if db_name not in rm_database]

for db_name in databases_final:
    current_db = myclient[db_name]
    collections = current_db.list_collection_names()

    for collection_name in collections:
        mycol = current_db[collection_name]
        mycol.drop()
print('### Clearing all databases ###')
