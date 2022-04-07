from azure.storage.fileshare import ShareFileClient
import os
from azure.identity import DefaultAzureCredential


ip_of_vm = "20.219.75.235"

def download_blob(bucket, file_path):
    service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectaccount;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name=bucket, file_path=file_path)
    with open(file_path, "wb") as file_handle:
        data = service.download_file()
        data.readinto(file_handle)

download_blob("deploymentbucket", "deployment-vm_key.pem")
print("pem file downloaded")

pwd = os.getcwd()


# os.system("sudo ssh -i deployment-vm_key.pem azureuser@20.219.75.235 &")

os.system("sudo scp  -i deployment-vm_key.pem setup.py azureuser@20.219.75.235:/home/azureuser")

os.system("cat setup.py | sudo  ssh azureuser@20.219.75.235 -i deployment-vm_key.pem python3 -")

print("setup started")



