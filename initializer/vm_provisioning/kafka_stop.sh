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

# SSH into VM
sshpass -f pass ssh -o StrictHostKeyChecking=no $USERNAME@$IP_ADDR "\
    cd kafka_2.13-3.1.0; \
    bin/zookeeper-server-stop.sh -daemon config/zookeeper.properties; \
    sleep 10s; \
    JMX_PORT=8004 bin/kafka-server-stop.sh -daemon config/server.properties; \
    sleep 10s;
"
    # bin/kafka-topics.sh --create --topic youtube --bootstrap-server $IP_ADDR:9092; \
    # exit
printf "\n"
echo "#### Succesfuly stopped kafka at VM $IP_ADDR ####"
printf "\n\n"