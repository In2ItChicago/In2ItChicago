#!/usr/bin/env bash

if [ ! "$(docker network ls | grep in2it)" ]
then
    docker swarm leave -f >/dev/null 2>&1
    if [ -x "$(command -v docker-machine)" ]; then
        # Sometimes docker machine complains about having multiple addresses
        docker swarm init --advertise-addr=$(docker-machine ip default)
    else
        docker swarm init
    fi
    docker network create --attachable --driver overlay in2it
    sleep 5
fi
