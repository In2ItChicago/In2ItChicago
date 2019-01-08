pip3 install -r requirements.txt
docker stack rm In2ItChicago
docker system prune -f
./scripts/stack-deploy.sh prod
