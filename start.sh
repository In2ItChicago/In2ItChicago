ENV=${1:-dev}
./scripts/create-network.sh
if [ "$CHECK_IMAGE_UPDATES" == "1" ]
then
    ./scripts/check-all-image-updates.sh
fi

./scripts/build-images.sh $ENV
docker-compose down
docker-compose rm -f -v
./db/run.sh &
./scripts/compose-deploy.sh --env dev "$@"
