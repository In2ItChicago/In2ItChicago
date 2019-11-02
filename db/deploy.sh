#!/bin/sh
if [ "$3" = "PROD" ]
then
    VOL="-v /var/run/postgresql:/var/run/postgresql"
else
    VOL=""
fi

docker run $1 --rm --network in2it --mount "type=bind,src=$(cd `dirname $0` && pwd),dst=/usr/src" $VOL \
    -e HOSTINGENV=$3 \
    --entrypoint /usr/src/entrypoint.sh db_deploy $2
