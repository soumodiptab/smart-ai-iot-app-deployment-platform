#!/bin/bash

# arr=$(sudo docker ps -a --filter "status=exited" -q)
# for i in "${arr[@]}"
# do
#    echo "$i"

# done

# for i in "${arr[@]}"
# do
#    sudo docker start $i

# done

while true
do
    arr=$(sudo docker ps -a --filter "status=exited" -q)
    # for i in "${arr[@]}"
    # do
    #     echo "$i"
    # done

    if [ ${#arr[@]} -gt 0 ]; then
        for i in "${arr[@]}"
        do
            sudo docker start $i
        done
    fi
    unset arr
    sleep 5
done