PARAMS=""
EVENT_PROCESSOR_DEBUG=0
SCHEDULER_DEBUG=0
VERBOSE_OUTPUT=0
EXCLUDE="ndscheduler"
RUN_SCHEDULER=0
ENV="dev"
SPIDER_NAME=""
while (( "$#" )); do
  case "$1" in
    -c|--scheduler-debug)
      SCHEDULER_DEBUG=1
      shift
      ;;
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
    -s|--scheduler)
      EXCLUDE=""
      RUN_SCHEDULER=1
      shift
      ;;
    -n|--spider-name)
      SPIDER_NAME=$2
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

if [ ! -z "$EXCLUDE" ] && [ -z "$PARAMS" ] 
then
    case "$(uname)" in
    CYGWIN*|MINGW*|MSYS*)
        # Carriage returns ruin everything
        SERVICES=$(docker-compose config --services | grep -v -e $EXCLUDE | tr '\r\n' ' ')
        ;;
    *)
        SERVICES=$(docker-compose config --services | grep -v -e $EXCLUDE)
        ;;
    esac
  
else
  SERVICES=$PARAMS
fi

SCHEDULER_DEBUG=$SCHEDULER_DEBUG \
EVENT_PROCESSOR_DEBUG=$EVENT_PROCESSOR_DEBUG \
VERBOSE_OUTPUT=$VERBOSE_OUTPUT \
RUN_SCHEDULER=$RUN_SCHEDULER \
SPIDER_NAME=$SPIDER_NAME \
docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml up $SERVICES
