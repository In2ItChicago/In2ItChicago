#!/bin/bash
ENV=${1:-dev}
if [ ! -d ./postgres_data ] then
    mkdir postgres_data
fi
docker stack rm In2ItChicago
sleep 5

./scripts/create-network.sh
./scripts/build-images.sh $ENV
./scripts/stack-deploy.sh $ENV
./db/run.sh DEV
