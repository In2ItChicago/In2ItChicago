#!/bin/sh
if [ "$1" = "DEV" ]
then 
    $(dirname $0)/../scripts/compose-deploy.sh --env dev postgres &
fi
$(dirname $0)/deploy.sh -i noconfirm $1
if [ "$1" = "DEV" ]
then
    docker-compose down
fi