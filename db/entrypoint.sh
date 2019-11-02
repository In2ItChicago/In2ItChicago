#!/bin/sh
if [ "$HOSTINGENV" = "DEV" ]
then
    until psql postgresql://postgres:postgres@postgres:5432/events -c "select 1" > /dev/null 2>&1; do
        echo "Waiting for postgres server..."
        sleep 1
    done
fi

cd /usr/src
python deploy.py $1