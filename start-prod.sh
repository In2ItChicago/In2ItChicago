pip3 install -r requirements.txt
scripts/render.sh
docker stack rm In2ItChicago
sleep 5
docker container prune -f
sleep 5

./scripts/create-network.sh
docker build -f db/Dockerfile -t db_deploy db
./db/run.sh &
./scripts/stack-deploy.sh prod
