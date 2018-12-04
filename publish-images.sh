./build-images.sh prod
docker tag data_engine in2itchicago/data_engine
docker tag clipboard_site in2itchicago/clipboard_site
docker tag clipboard_db_client in2itchicago/clipboard_db_client
docker push in2itchicago/data_engine
docker push in2itchicago/clipboard_site
docker push in2itchicago/clipboard_db_client