#!/bin/bash

printf "\n\n\n\n"
echo "####### Welcome to the Smart AI IOT App Deployment Platform ########"
printf "\n\n\n\n"

az login

printf "\n"
echo "Enter the resource group name to delete"
read RESOURCE_GROUP_NAME

printf "\n"
echo "## Deleting all the VMs inside resource group ##"
# delete all vms in that resource group without any prompt
az vm delete --ids $(az vm list -g $RESOURCE_GROUP_NAME --query "[].id" -o tsv) --yes

printf "\n"
echo "## Deleting the resource group ##"
# delete the resource group
az group delete --name $RESOURCE_GROUP_NAME --yes

printf "\n"
echo "## Clearing the contents of the vm_details file ##"
# clear the contents of file
filename='vm_details.txt'  
truncate -s 0 $filename

