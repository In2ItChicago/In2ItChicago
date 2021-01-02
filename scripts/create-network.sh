#!/usr/bin/env bash

if [ ! "$(docker network ls | grep in2it)" ]
then
    docker swarm leave -f >/dev/null 2>&1
    docker swarm init --advertise-addr 127.0.0.1
    docker network create --attachable --driver overlay in2it
    sleep 5
fi
