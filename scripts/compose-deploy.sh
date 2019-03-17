PARAMS=""
EVENT_PROCESSOR_DEBUG=0
VERBOSE_OUTPUT=0
ENV="dev"
while (( "$#" )); do
  case "$1" in
    -d|--processor-debug)
      EVENT_PROCESSOR_DEBUG=1
      shift
      ;;
    -e|--env)
      ENV=$2
      shift 2
      ;;
    -v|--verbose-output)
      VERBOSE_OUTPUT=1
      shift
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
if [ ! "$(docker network ls | grep in2it)" ]; then
  docker network create in2it
fi
EVENT_PROCESSOR_DEBUG=$EVENT_PROCESSOR_DEBUG \
VERBOSE_OUTPUT=$VERBOSE_OUTPUT \
docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up $PARAMS
