#!/bin/bash
$(dirname $0)/../scripts/compose-deploy.sh --env dev postgres &
$(dirname $0)/deploy.sh -i noconfirm
docker-compose down
