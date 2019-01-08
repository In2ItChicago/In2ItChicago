docker build -t event_processor event_processor
docker build -t in2it_site in2it_site --target=in2it_site_$1
docker build -t event_service event_service