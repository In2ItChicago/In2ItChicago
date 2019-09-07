#!/bin/bash
# dummy environment variables
export SCHEDULE_INTERVAL=5
cd ./event_processor
python3 ./generate_docs.py 