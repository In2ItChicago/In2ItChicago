#!/bin/bash
ENV=${1:-dev}
docker stack rm In2ItChicago
sleep 5

./scripts/create-network.sh
./scripts/build-images.sh $ENV
./db/run.sh &
./scripts/stack-deploy.sh $ENV