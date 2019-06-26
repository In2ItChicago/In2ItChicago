#!/bin/bash
if [ ! "$(docker network ls | grep in2it)" ]
then
    if [ -x "$(command -v docker-machine)" ]; then
        # Sometimes docker machine complains about having multiple addresses
        docker swarm init --advertise-addr=$(docker-machine ip default)
    else
        docker swarm init
    fi
    docker network create --attachable --driver overlay in2it
    sleep 5
fi