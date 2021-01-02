#!/usr/bin/env bash
set -e

./scripts/create-network.sh
docker stack rm In2ItChicago
sleep 5
docker container prune -f
sleep 5

docker build -f db/Dockerfile -t db_deploy db
docker build -f create_schedules/Dockerfile -t create_schedules create_schedules
docker build -f caddy/Dockerfile -t caddy_config caddy
env $(cat .env-prod | xargs) ./scripts/stack-deploy.sh prod
./db/run.sh PROD
