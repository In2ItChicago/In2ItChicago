pip3 install -r requirements.txt
scripts/render.sh
docker stack rm In2ItChicago
sleep 5
docker system prune -f
sleep 5
./scripts/stack-deploy.sh prod
