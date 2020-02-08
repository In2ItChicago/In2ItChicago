#!/usr/bin/env bash
set -e

PARAMS=""
PARAMS_COPY="$@"
while (( "$#" )); do
  if [[ "$1" == -* ]]
  then
    shift 2
  else
    PARAMS="$PARAMS $1"
    shift
  fi
done
#set positional arguments in their proper place
eval set -- "$PARAMS"

docker-compose stop $PARAMS
docker-compose rm -f -v $PARAMS
./scripts/build-images.sh dev
./scripts/compose-deploy.sh --env dev $PARAMS_COPY