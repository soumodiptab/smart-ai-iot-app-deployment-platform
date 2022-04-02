# pip install azure-storage-file-share
# pip install azure-identity

from azure.storage.fileshare import ShareFileClient
import os
from azure.identity import DefaultAzureCredential

# service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectstorage;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name="<bucket-name>", file_path="<filename-after-upload>")

service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectaccount;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name="aibucket", file_path="1.zip")

# Upload a blob
# with open("4c8a22edb162477190d611387148c0d7.zip", "rb") as source_file:
#     service.upload_file(source_file)

# Download a blob
# with open("2.zip", "wb") as file_handle:
#     data = service.download_file()
#     data.readinto(file_handle)

def upload_blob(file_path):
    service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectaccount;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name="aibucket", file_path=file_path)
    with open(file_path, "rb") as source_file:
        service.upload_file(source_file)

def download_blob(file_path):
    service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectaccount;AccountKey=3m7pA/FPcLIe195UhnJ7bZUMueN8FBPBpKUF42lsEP9xk3ZWzM3XpeSh4NWq+cOOitaLmJbU7hJ2UWLdrVL8NQ==;EndpointSuffix=core.windows.net", share_name="aibucket", file_path=file_path)
    with open(file_path, "wb") as file_handle:
        data = service.download_file()
        data.readinto(file_handle)

# with open("deployer.log", "rb") as source_file:
#     service.upload_file(source_file)

# with open("deployer2.log", "wb") as file_handle:
#     data = service.download_file()
#     data.readinto(file_handle)