# smart-ai-iot-app-deployment-platform

A distributed microservices-based platform that allows ML models to be deployed as a service and also enables IoT devices to be deployed. It allows App developers to build smart apps like Intruder Prevention System, Smart Classroom and Smart Home using an SDK provided by the platform.

The platform comes with some documentation that species the various artifacts to be in a specific format.

## Roles:

1. AI Developer: Creates ML models and wants to deploy these models on our platform.
2. App Developer: Creates ML-Apps that use these models and IoT device and is deployed on the platform.
3. Platform Configurer: Administrator that registers these IoT devices on the platform and registers other kinds of users.
4. End-user: Selects and Schedules the app where it will be deployed and when i.e.day, time of day and how many times.

## The flow of events:
### Ai event flow:
1. Create an ML model and test it in Collab/Notebook.
2. Login as an AI developer onto the platform.
3. The AI dev follows the SDK notations to create the AI model.
4. Artifacts are uploaded as a zip which contains JSON config files that specify the name of the API and how to use it.
the zip file is uncompressed and verified of the nomenclature and JSON configs.
5. A wrapper service is used to convert the model into a REST endpoint.
6. The zip is uploaded to the file bucket using Azure blob and a new deployment message is sent over Kafka to the deployer service.
7. The deployer downloads the zip unpacks it, and adds the SDK files like logging, monitoring heartbeat and libraries for communication over REST.
8. The model started as a docker service on one of the servers.
### Sensor/Controller events:
1. Platform configurer registers IoT devices like sensors and controllers on the platform.
2. Sensors are input devices and controllers are output devices. The P.C. has to enter the type of device, its input parameters for controllers and output parameters for sensors.
3. Once sensor controllers are registered, the P.C. has to select the location where the devices can be deployed it can be a traffic junction, a school or a bank.
4. Once the device instances are provided a comm. link is established with these devices. The comm. is over Kafka and the devices use the platform SDK files to comm.
5. We created our own Sensor and Controllers using our own simulators : Camera Sensor,light sensor,temperature and Controllers like fan, display, AC.

### App events:
1. App developer can browse the platform to see the available ML models that are provided as REST endpoints using hash-id.
Just like models IOT devices are also provided with with their own ids.
2. To use models,sensor and controllers they simply need to use the provided platform SDK like:
```python
from platform_sdk import *
res=model_call(“id”,params=[,])
```
3. The app developer also needs to declare a json file just like Java Spring context files that maps each model to its identifying code.
4. The app can be a backend app or a web app with its own features and UI pages.
5. The artifacts of the app are zipped and uploaded.
6. The zip is verified and uploaded to a file bucket.
### App deployment events:
1. End user opens the platform and sees a list of apps that are available.
2. They select the app and the location where they want the sensors and controllers to be present. It has to be selected from a list of available locations where the IOT devices are already deployed.
3. They also need to provide date and time of deployment and frequency of starting that is twice per day and start and end time.
4. Once they select all these, the schedule the app.
5. In the backend the sensors and controllers are bound to the app using an instance id that is used by the SDK to route the calls to the IOT devices.
6. This way multiple apps can use the same IOT device.
7. A deployment message is sent to the scheduler.
8. The scheduler uses chron job schedule different apps.
9. Once an app’s time arrives the chron job is activated which sends a message to the deployer for deployment.
10. Deployer searches the app in file bucket using app-id and uncompresses the artifacts,loads the libraries : SDK,logger,heartbeat,monitoring,email service
11. The app is started as a docker service on a server using a load balancer.
12. Once the app is started its address is sent to the end user via email.
### App operations:
1. Once app is started the sensor sends data to the app using the SDK over kafka.
2. the messages are encoded and decoded according to data like images are converted to bin and decoded back into pixels.
3. The app can use the models via the rest end points that use the SDK to translate the model-id it to its actual ip address and REST endpoint name.
4. A heartbeat service is hooked into all apps,models and infra services that monitors the failure of a service and automatically restarts it when failed.
5. A logger service is built-in the platform and also provided in the SDK that collects logs across all services and collects them inside a file bucket to be used to deduce job failures.

## Important Components:

### BootStrapper: 
* A script based service that runs on a host. 
* Once launched it uses Azure SDK to create VM Servers. 
* A main server is created that hosts important stuff like Node manager, Heartbeat Service and load balancer.
* It launches the main script on Main server. This script installs all libraries on all servers by using ssh and pulls the repo using git
* The init script launches node manager that contains the load balancer module and the monitoring service i.e. heartbeat/fault tolerance.
* It also starts the service agent,node agent on each server/node using ssh
### Node manager(load balancer): 
loads the service roster and assigns it a VM/node using load balancer where server with least load is chosen. 
Once a server is selected for a service it is sent via kafka to service agent.
### Service Agent/Node agent: 
* Kafka based message processor that starts a service using docker, all it needs is service name and it will start the service by locating it in the repository. 
* Services can be: deployer,scheduler,ai manager,platform front end,device manager,app manager.
* It also has a flask server running which gives node manager info. of load on each server like how many processes, how much ram ,cpu usage is there.
* These are required by the load balancer.
### Deployer:
* Can deploy model/app requires instance id and app/model id
* Builder service that generates docker files using json configs.
* hooks the platform sdk into the app.
* generates dynamic json config that are required by the app.
* launches the app as a docker container on the server with least load using service agent.  
### Scheduler:
* Chron job based docker service that schedules apps
* The app that is ready to be deployed is sent via message to deployer.
* Email Service: Converts Kafka messages to emails.
### Logger:
* Distributed logger that uses kafka to send logs over kafka msg queues, the logs are generated using the python logger but with some modifications.
* Logs are collected using the logger main service at main server and saved in a file bucket.
### Monitoring/Fault Tolerance: using heartbeat service
* Each service has the heartbeat service hooked into it.
* Heartbeat Server and client works together.
* When any service starts the heartbeat client registers its service using the service-id to the server. 
* Then it starts sending some echo messages after a set interval.
* The server recieves these messages by creating a new thread object.
* If it doesnt recieve a msg after a particular RTT/ interval then it queries the node manager of the location of the service and sends a restart message for that service to its corresponding service agent.
* The agent locates the docker container that failed and restarts it.
### Web Server : 
Hosts all web pages and REST endpoints for the different roles/users to suthenticate and start some operations.
### Horizontal scaling:  
* Azure SDK is used to create a new VM and it to the pool of VM’s incase load increases in all VM’s beyond a set threshold. 
* There is downtime for the service/app that needs to be started because of the new VM creation.
