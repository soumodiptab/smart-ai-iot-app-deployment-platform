from azure.storage.fileshare import ShareFileClient
import os
import zipfile


ip_of_vm = "20.219.75.235"

service_name = "test-deploy"

def download_blob(bucket, file_path):
    file_path = service_name + ".zip"
    print(file_path)
    service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectaccount;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name=bucket, file_path=file_path)
    with open(file_path, "wb") as file_handle:
        data = service.download_file()
        data.readinto(file_handle)

def unzip_run_app(app_zip_file):
    app_zip_full_path = os.getcwd() + "/" + app_zip_file + ".zip"
    print(app_zip_full_path)

    dest_path = os.getcwd() + "/" + service_name
    with zipfile.ZipFile(app_zip_full_path, "r") as zipobj:
        zipobj.extractall(dest_path)    

download_blob("deploymentbucket", service_name)
print("file downlaoded")
unzip_run_app(service_name)
print("file unzipped")


import os

print("installing requirements")
os.system("pip install -r {}/requirements.txt".format(service_name))
print("starting service")
os.system("python3 {}/flask_server.py &".format(service_name))