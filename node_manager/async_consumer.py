from aiokafka import AIOKafkaConsumer
import asyncio
import socket

def getSelfIp():   
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 

    return IPAddr
async def consume():
    self_ip = getSelfIp()
    print("Self-ip", self_ip)
    consumer = AIOKafkaConsumer(
        'deploy_'+self_ip,
        bootstrap_servers='13.71.109.62:9092')
    # Get cluster layout and join group `my-group`
    print("trying1")
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)


            print("consuming")
            msg = message.value
            app_id = msg["app_id"]
            app_instance_id = msg["app_instance_id"]
            is_model = msg["isModel"]

            if is_model:
                getAppZipFromStorage(app_id, "aibucket")
            else:
                getAppZipFromStorage(app_id, "appbucket")

            updateNodeDeploymentStatus(app_id, app_instance_id, self_ip, free_port, "Success")
    finally:
    	print("trying2")
    	await consumer.stop()
asyncio.run(consume())