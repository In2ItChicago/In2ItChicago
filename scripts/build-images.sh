docker build "${@:2}" -t event_processor event_processor
docker build "${@:2}" -t in2it_site in2it_site --target=in2it_site_$1
docker build "${@:2}" -t event_service event_service