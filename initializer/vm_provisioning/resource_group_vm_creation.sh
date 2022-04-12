#!/bin/bash

printf "\n\n\n\n"
echo "####### Welcome to the Smart AI IOT App Deployment Platform ########"
printf "\n\n\n\n"

az login

SUB_ID=$(az account show --query 'id' -o json)

printf "\n\n"
echo "###### Provisioning VMs ########"
printf "\n\n"

printf "\n"
echo "Enter the resource group name to create"
read RESOURCE_GROUP_NAME

az group create --name $RESOURCE_GROUP_NAME --location southindia

VM_NAMES=( "VM3" "VM4" )
# VM_NAMES=( "VM_kafka" )
VM_PUBLIC_IPs=()

printf "\n\n"
echo "## Provisioning ${#VM_NAMES[@]} VMs ##"
printf "\n"

for vm_name in "${VM_NAMES[@]}"
do
PUBLIC_IP_ADDRESS=$(az vm create --resource-group $RESOURCE_GROUP_NAME \
  --name $vm_name \
  --image UbuntuLTS \
  --output json \
  --verbose \
  --public-ip-sku Standard \
  --authentication-type all\
  --generate-ssh-keys\
  --admin-password password123@\
  --query 'publicIpAddress' -o json)


VM_PUBLIC_IPs+=($PUBLIC_IP_ADDRESS)
az vm open-port --port 80 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 600
az vm open-port --port 2376 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 700
az vm open-port --port 9092 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 800
az vm open-port --port 27017 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1000
az vm open-port --port 8004 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1200
az vm open-port --port 10000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1100
az vm open-port --port 50000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1300
done

printf "\n\n"
echo "VMs have been provisioned at following IP addresses"
OUTPUT_FILENAME=vm_details.txt
VM_ADMIN_USERNAME=$(az vm show --resource-group $RESOURCE_GROUP_NAME --name ${VM_NAMES[0]} --query 'osProfile.adminUsername' -o json)
VM_ADMIN_USERNAME=$(echo "$VM_ADMIN_USERNAME" | tr '"' "'")

for ip in "${VM_PUBLIC_IPs[@]}"
do
  IP_NEW="${ip%\"}"
  IP_NEW="${IP_NEW#\"}"
  UN_NEW="${VM_ADMIN_USERNAME%\'}"
  UN_NEW="${UN_NEW#\'}"
  echo $IP_NEW
  echo $UN_NEW
  sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "sudo apt install curl; curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh; sudo apt-get install sshpass; sudo apt install -y python3-pip; sudo -H pip3 install --upgrade pip; sudo apt-get -y install mongodb; sudo apt-get update; sudo service mongodb start;"
  
#   sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "sudo apt install curl; curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh; sudo apt-get install sshpass; sudo apt install -y python3-pip;sudo -H pip3 install --upgrade pip; chmod +x ./mongodb_install.sh; ./mongodb_install.sh;"
  # sshpass -f pass scp -o StrictHostKeyChecking=no -r node $UN_NEW@$IP_NEW:node
  # sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "cd node && python3 node2.py" &
done

INDEX=0
for ip in "${VM_PUBLIC_IPs[@]}"
do
  echo "* $ip"
  ip=$(echo "$ip" | tr '"' "'")
  echo "$ip '${VM_NAMES[$INDEX]}' $VM_ADMIN_USERNAME" >> $OUTPUT_FILENAME
  INDEX=$((INDEX+1))
done

# Run the VMs
chmod +x ./vm_start.sh
./vm_start.sh
