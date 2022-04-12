#!/bin/bash
# $1: IP of the VM
# $2: VM name

while IFS= read -r line; 
do
    IP_ADDR="$(echo $line | cut -d' ' -f1)" 
    #removing '' from IP_ADDR
    IP_ADDR="${IP_ADDR%\'}"
    IP_ADDR="${IP_ADDR#\'}"

    VM_NAME="$(echo $line | cut -d' ' -f2)"
    VM_NAME="${VM_NAME%\'}"
    VM_NAME="${VM_NAME#\'}"

    USERNAME="$(echo $line | cut -d' ' -f3)"
    USERNAME="${USERNAME%\'}"
    USERNAME="${USERNAME#\'}"

    SERVICE="$(echo $line | cut -d' ' -f4)"
    SERVICE="${SERVICE%\'}"
    SERVICE="${SERVICE#\'}"


    if [ "$SERVICE" = "kafka" ]; then
      break
    fi
done < kafka_vm_details.txt

printf "\n\n"
echo "##### Deploying kafka at VM $IP_ADDR ####"
printf "\n\n"

# transfer python file updater
scp ./kafka_params_updater.py $USERNAME@$IP_ADDR:/home/$USERNAME


# SSH into VM
sshpass -f pass ssh -o StrictHostKeyChecking=no $USERNAME@$IP_ADDR "\
    sudo apt install -y default-jre; \
    wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz; \
    tar -xzf kafka_2.13-3.1.0.tgz; \
    python3 kafka_params_updater.py $IP_ADDR; \
    cd kafka_2.13-3.1.0; \
    bin/zookeeper-server-start.sh -daemon config/zookeeper.properties; \
    sleep 10s; \
    JMX_PORT=8004 bin/kafka-server-start.sh -daemon config/server.properties; \
    sleep 10s;
"
    # bin/kafka-topics.sh --create --topic youtube --bootstrap-server $IP_ADDR:9092; \
    # exit
printf "\n"
echo "#### Succesfuly deployed kafka at VM $IP_ADDR ####"
printf "\n\n"