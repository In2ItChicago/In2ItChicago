ARGS=("$@")
docker-compose -f docker-compose.yml -f docker-compose.${ARGS[0]}.yml up ${ARGS[@]:1}
