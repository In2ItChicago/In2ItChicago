docker run -it --rm --network In2ItChicago_in2it --mount "type=bind,src=$(pwd),dst=/usr/src" --entrypoint /usr/src/entrypoint.sh db_deploy
