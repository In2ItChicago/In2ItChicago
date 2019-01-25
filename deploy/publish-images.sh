$(dirname $0)/../scripts/build-images.sh prod
docker tag event_processor_prod in2itchicago/event_processor:$1
docker tag in2it_site_prod in2itchicago/in2it_site:$1
docker tag event_service_prod in2itchicago/event_service:$1
docker push in2itchicago/event_processor
docker push in2itchicago/in2it_site
docker push in2itchicago/event_service