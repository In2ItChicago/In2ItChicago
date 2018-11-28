docker-compose down
docker system prune -f
./render.sh
docker-compose build
docker-compose up -d
