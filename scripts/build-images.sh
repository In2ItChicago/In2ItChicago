docker build "${@:2}" -f event_processor/build_$1/Dockerfile -t event_processor event_processor
docker build "${@:2}" -f in2it_site/build_$1/Dockerfile -t in2it_site in2it_site
docker build "${@:2}" -f event_service/build_$1/Dockerfile -t event_service event_service