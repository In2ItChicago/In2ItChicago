PARAMS=""
DATA_ENGINE_DEBUG=0
ENV="dev"
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
DATA_ENGINE_DEBUG=$DATA_ENGINE_DEBUG docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up $PARAMS
