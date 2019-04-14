$(dirname $0)/../scripts/build-images.sh prod
$(dirname $0)/../../ndscheduler/build.sh prod
docker tag event_processor_prod in2itchicago/event_processor:$1
docker tag in2it_site_prod in2itchicago/in2it_site:$1
docker tag event_service_prod in2itchicago/event_service:$1
docker tag ndscheduler_prod in2itchicago/ndscheduler:$1