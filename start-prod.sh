#!/usr/bin/env bash
set -e

./scripts/create-network.sh
docker stack rm In2ItChicago
sleep 5
docker container prune -f
sleep 5

docker build -f db/Dockerfile -t db_deploy db
source .env-prod && ./scripts/stack-deploy.sh prod
./db/run.sh PROD
