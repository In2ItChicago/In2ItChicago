docker run $1 --rm --network clipboardapp_in2it --mount "type=bind,src=$(cd `dirname $0` && pwd),dst=/usr/src" --entrypoint /usr/src/entrypoint.sh db_deploy $2
