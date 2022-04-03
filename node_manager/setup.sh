kill -9 $(ps aux|grep '[p]ython3 deployer.py' | awk ' { print $2 } ')
python3 node_manager/deployer.py &
sleep 1

kill -9 $(ps aux|grep '[p]ython3 node_manager.py' | awk ' { print $2 } ')
python3 node_manager/node_manager.py &
sleep 1

kill -9 $(ps aux|grep '[p]ython3 node_agent.py' | awk ' { print $2 } ')
python3 node_manager/node_agent.py &
sleep 1
