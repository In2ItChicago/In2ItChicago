docker-compose down
./build-images.sh
./render.sh
docker-compose build
docker-compose up -d
