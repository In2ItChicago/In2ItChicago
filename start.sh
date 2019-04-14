if [ ! "$(docker network ls | grep in2it)" ]
then
  docker network create --attachable --driver overlay in2it
fi

if [ -f ../ndscheduler/build.sh ]
then
  ../ndscheduler/build.sh dev
fi
./scripts/build-images.sh dev
./scripts/check-all-image-updates.sh
docker-compose rm -f -v
./db/run.sh &
./scripts/compose-deploy.sh --env dev "$@"
