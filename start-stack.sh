#!/bin/bash
ENV=${1:-dev}
docker stack rm In2ItChicago
sleep 5

./scripts/create-network.sh
./scripts/build-images.sh $ENV
./db/run.sh &
DB_PID=$!
./scripts/stack-deploy.sh $ENV
echo "Waiting for db deploy. PID: ${DB_PID}"
wait $DB_PID
