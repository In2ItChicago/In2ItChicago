#!/usr/bin/env bash
set -e

docker push in2itchicago/in2it_site:$1
docker push in2itchicago/event_service:$1
docker push in2itchicago/ndscheduler:$1