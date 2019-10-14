#!/bin/bash
if [ ! -d ./postgres_data ]; then
    mkdir postgres_data
fi

docker stack rm In2ItChicago
sleep 5
docker container prune -f
sleep 5

./scripts/create-network.sh
docker build -f db/Dockerfile -t db_deploy db
./scripts/stack-deploy.sh prod
./db/run-prod.sh
