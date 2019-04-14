docker stack rm In2ItChicago
sleep 5
ENV=${1:-dev}

if [ ! "$(docker network ls | grep in2it)" ]
then
  docker network create --attachable --driver overlay in2it
fi

if [ -f ../ndscheduler/build.sh ]
then
  ../ndscheduler/build.sh $ENV
fi

./scripts/build-images.sh $ENV
./scripts/check-all-image-updates.sh
./db/run.sh &
./scripts/stack-deploy.sh $ENV