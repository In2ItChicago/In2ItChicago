docker run $1 --rm --network in2it --mount "type=bind,src=$(cd `dirname $0` && pwd),dst=/usr/src" --entrypoint /usr/src/entrypoint.sh db_deploy $2
