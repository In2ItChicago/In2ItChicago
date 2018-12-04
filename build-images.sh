docker build -t data_engine data_engine --progress=plain
docker build -t clipboard_site clipboard_site --target=clipboard_site_$1 --progress=plain
docker build -t clipboard_db_client clipboard_db_client --progress=plain
docker tag data_engine aschey/data_engine
docker tag clipboard_site aschey/clipboard_site
docker tag clipboard_db_client aschey/clipboard_db_client
docker push aschey/data_engine
docker push aschey/clipboard_site
docker push aschey/clipboard_db_client