#!/bin/bash
if [ ! "$(docker network ls | grep in2it)" ]
then
  docker swarm init
  docker network create --attachable --driver overlay in2it
  sleep 5
fi