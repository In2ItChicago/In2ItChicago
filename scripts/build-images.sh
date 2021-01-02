#!/usr/bin/env bash
set -e

EXTRA_ARGS="${@:2}"
ENV="$1"

function build-cmd {
  echo "docker build $EXTRA_ARGS -f $2/$1/Dockerfile -t $1_$ENV --build-arg BUILD_ENV=$ENV --target $1_$ENV $2/$1"
}

if [ -f ../ndscheduler/Dockerfile ]
then
  DOCKER_BUILDKIT=1 $(build-cmd ndscheduler ..)
fi
DOCKER_BUILDKIT=1 $(build-cmd in2it_site .)
DOCKER_BUILDKIT=1 $(build-cmd event_service .)
DOCKER_BUILDKIT=1 docker build -f caddy/Dockerfile -t caddy_config caddy
DOCKER_BUILDKIT=1 docker build -f create_schedules/Dockerfile -t create_schedules create_schedules
DOCKER_BUILDKIT=1 docker build -f db/Dockerfile -t db_deploy db