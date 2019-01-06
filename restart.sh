PARAMS=""
DATA_ENGINE_DEBUG=0
ENV="dev"
PARAMS_COPY="$@"
while (( "$#" )); do
  case "$1" in
    -dd|--data-engine-debug)
      DATA_ENGINE_DEBUG=$2
      shift 2
      ;;
    -e|--env)
      ENV=$2
      shift 2
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

docker-compose stop $PARAMS
docker-compose rm -f -v $PARAMS
./scripts/build-images.sh dev
./scripts/compose-deploy.sh --env dev $PARAMS_COPY