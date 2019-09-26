#!/bin/bash
until $(curl --output /dev/null --silent --head --fail http://in2it_site:3000); do
    printf 'Waiting for in2it site...'
    sleep 5
done
printf "\n%s\n"  "Site is online"

until $(curl --output /dev/null --silent --head --fail http://event_service:5000/events); do
    printf 'Waiting for API...'
    sleep 5
done
printf "\n%s\n"  "API is online"

python3 ./render.py nginx.conf.j2
nginx -c /etc/nginx/nginx.conf -t
running=$(service nginx status)
if [ "$running" = "nginx is running." ]
then
    /etc/init.d/nginx-debug reload
else
    service nginx-debug start
fi