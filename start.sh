./scripts/create-network.sh
if [ "$CHECK_IMAGE_UPDATES" == "1" ]
then
    ./scripts/check-all-image-updates.sh
fi

./scripts/build-images.sh dev
docker-compose down
docker-compose rm -f -v
./db/run.sh &
./scripts/compose-deploy.sh --env dev "$@"
