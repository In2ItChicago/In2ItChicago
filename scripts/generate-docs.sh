#!/usr/bin/env bash
# dummy environment variables
export SCHEDULE_INTERVAL=5 

#delete the old docs folder??? 
sudo rm -rf ./docs 
# make a master docs directory
mkdir ./docs

# generate docs for event_processor
echo "Generating docs for event_processor..."
event_processor_id=$(docker container ls -q --filter "name=event_processor")
sudo rm -rf ./event_processor/docs
docker exec -t $event_processor_id pdoc3 --html --force --output-dir docs event_processor
# move generated docs into master docs folder
sudo chmod +w ./event_processor/docs
sudo mv -u ./event_processor/docs/* ./docs
sudo rm -rf ./event_processor/docs
echo "Moved event_processor docs to the /docs folder..."

# generate docs for event_service 
echo "Generating docs for event_service..."
event_service_id=$(docker container ls -q --filter "name=event_service")
sudo rm -rf ./event_service/docs
docker exec -t $event_service_id npm run generatedocs
# typedoc doesn't create a root folder, so one is created manually
mkdir ./docs/event_service 
sudo mv -u ./event_service/docs/* ./docs/event_service
sudo rm -rf ./event_service/docs
echo "Moved event_service docs to the /docs folder..."

# generate docs for in2it_site 
echo "Generating docs for in2it_site..."
in2it_id=$(docker container ls -q --filter "name=in2it_site")
sudo rm -rf ./in2it_site/docs
docker exec -t $in2it_id npx jsdoc ./ -r -c jsdoc-conf.json 
mkdir ./docs/in2it_site 
sudo mv -u ./in2it_site/docs/* ./docs/in2it_site
sudo rm -rf ./in2it_site/docs
echo "Moved in2it_site docs to the /docs folder..."

