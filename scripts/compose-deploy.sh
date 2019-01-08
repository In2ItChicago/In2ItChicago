PARAMS=""
EVENT_PROCESSOR_DEBUG=0
VERBOSE_OUTPUT=0
RUN_SCHEDULER=1
ENV="dev"
while (( "$#" )); do
  case "$1" in
    -dd|--data-engine-debug)
      EVENT_PROCESSOR_DEBUG=$2
      shift 2
      ;;
    -e|--env)
      ENV=$2
      shift 2
      ;;
    -v|--verbose-output)
      VERBOSE_OUTPUT=$2
      shift 2
      ;;
    -s|--run-scheduler)
      RUN_SCHEDULER=$2
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
EVENT_PROCESSOR_DEBUG=$EVENT_PROCESSOR_DEBUG \
VERBOSE_OUTPUT=$VERBOSE_OUTPUT \
RUN_SCHEDULER=$RUN_SCHEDULER \
docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up $PARAMS
