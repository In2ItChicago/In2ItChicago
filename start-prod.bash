pip3 install -r requirements.txt
docker stack rm ClipboardApp
docker system prune -f
./scripts/stack-deploy.sh prod
