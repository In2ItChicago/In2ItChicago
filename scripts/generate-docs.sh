#!/bin/bash
# dummy environment variables
export SCHEDULE_INTERVAL=5 

#delete the old docs folder??? 
rm -rf ./docs 
# make a master docs directory
mkdir ./docs

# generate docs for event_processor
echo "Generating docs for event_processor..."
event_processor_id=$(docker container ls -q --filter "name=event_processor")
docker exec -t $event_processor_id pdoc3 --html --force --html-dir docs event_processor
# move generated docs into master docs folder
mv -u ./event_processor/docs/* ./docs
echo "Moved event_processor docs to the /docs folder..."

# generate docs for event_service 
echo "Generating docs for event_service..."
event_service_id=$(docker container ls -q --filter "name=event_service")
docker exec -t $event_service_id npm run generatedocs
# typedoc doesn't create a root folder, so one is created manually
mkdir ./docs/event_service 
mv -u ./event_service/docs/* ./docs/event_service
echo "Moved event_service docs to the /docs folder..."



