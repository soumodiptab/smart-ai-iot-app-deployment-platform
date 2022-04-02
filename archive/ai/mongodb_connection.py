# importing module
from pymongo import MongoClient
  
# creation of MongoClient
client=MongoClient()
  
# Connect with the portnumber and host
client = MongoClient("mongodb://localhost:27017/")
  
db = client["med_data"]

my_collection = db["patient_data"]

patient_record = {
   "Name": "Maureen Skinner",
   "Age": 87,
   "Sex": "F",
   "Blood pressure": [{"sys": 156}, {"dia": 82}],
   "Heart rate": 82
}

my_collection.insert_one(patient_record)

for item in my_collection.find():
    print(item)

