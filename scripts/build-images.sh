#!/bin/bash
if [ -f ../ndscheduler/build.sh ]
then
  ../ndscheduler/build.sh $1
fi
docker build "${@:2}" -f event_processor/build_$1/Dockerfile -t event_processor_$1 event_processor
docker build "${@:2}" -f in2it_site/build_$1/Dockerfile -t in2it_site_$1 in2it_site
docker build "${@:2}" -f event_service/build_$1/Dockerfile -t event_service_$1 event_service
if [ "$1" == "dev" ]
then
    docker build "${@:2}" -f nginx/build_$1/Dockerfile -t nginx_$1 nginx
fi
docker build -f db/Dockerfile -t db_deploy db