#!/usr/bin/env bash
EVENT_PROCESSOR_DEBUG=0 \
VERBOSE_OUTPUT=0 \
RUN_SCHEDULER=1 \
docker stack deploy --compose-file docker-compose.yml --compose-file docker-compose.$1.yml In2ItChicago
