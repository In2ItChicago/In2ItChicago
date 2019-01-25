docker build "${@:2}" -f event_processor/build_$1/Dockerfile -t event_processor_$1 event_processor
docker build "${@:2}" -f in2it_site/build_$1/Dockerfile -t in2it_site_$1 in2it_site
docker build "${@:2}" -f event_service/build_$1/Dockerfile -t event_service_$1 event_service