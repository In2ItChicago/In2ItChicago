docker build -t data_engine data_engine
docker build -t clipboard_site clipboard_site --target=clipboard_site_$1
docker build -t clipboard_db_client clipboard_db_client