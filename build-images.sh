docker build -t data_engine -f data_engine/Dockerfile .
docker build -t clipboard_db_client -f clipboard_db_client/Dockerfile .
docker build -t clipboard_site -f clipboard_site/Dockerfile .