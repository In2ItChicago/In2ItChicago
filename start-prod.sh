#!/bin/bash
pip3 install -r requirements.txt
if [ ! -d ./postgres_data ]; then
    mkdir postgres_data
fi
scripts/render.sh
docker stack rm In2ItChicago
sleep 5
docker container prune -f
sleep 5

./scripts/create-network.sh
docker build -f db/Dockerfile -t db_deploy db
./scripts/stack-deploy.sh prod
./db/run-prod.sh
