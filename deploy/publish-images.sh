#!/usr/bin/env bash
set -e

docker push in2itchicago/in2it_site
docker push in2itchicago/event_service
docker push in2itchicago/ndscheduler