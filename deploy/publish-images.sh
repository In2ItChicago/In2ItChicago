$(dirname $0)/../scripts/build-images.sh prod --no-cache
docker tag event_processor in2itchicago/event_processor
docker tag in2it_site in2itchicago/in2it_site
docker tag event_service in2itchicago/event_service
docker push in2itchicago/event_processor
docker push in2itchicago/in2it_site
docker push in2itchicago/event_service