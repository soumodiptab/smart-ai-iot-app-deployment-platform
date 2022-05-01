#!/bin/bash  

file='vm_details.txt'  
  
i=1  
while read line; do  
  
#Reading each line  
echo "Line No. $i : $line"  
i=$((i+1))  
done < $file  


VM_PUBLIC_IPs=()
VM_ADMIN_USERNAME=()


line_no=$(cat ${file} | wc -l)
#echo ${line_no}

IFS=$'\n' read -d '' -r -a lines < $file

for ((i = 1 ; i <= $line_no ; i++)); do
		arr=(${lines[i-1]})
  		VM_PUBLIC_IPs+=(${arr[0]})
  		VM_ADMIN_USERNAME+=(${arr[2]})
  		
done

for ((i = 1 ; i <= $line_no ; i++)); do
		IP_NEW=${VM_PUBLIC_IPs[i-1]}
		#echo $IP_NEW
		IP_NEW="${IP_NEW%\'}"
		IP_NEW="${IP_NEW#\'}"
		UN_NEW=${VM_ADMIN_USERNAME[i-1]}
		#echo $UN_NEW
		UN_NEW="${UN_NEW%\'}"
		UN_NEW="${UN_NEW#\'}"
		echo $IP_NEW
		echo $UN_NEW
		# sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW 'rm -R node;'
		sshpass -f pass scp -o StrictHostKeyChecking=no -r node $UN_NEW@$IP_NEW:node
		gnome-terminal --title="node-$IP_NEW" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW 'ps; /bin/bash'"
		# gnome-terminal --title="node-$IP_NEW" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW 'ps;cd node;pip3 install -r requirements.txt; /bin/bash'"

done

python3 subsystem_database_entry.py