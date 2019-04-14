# This file ends in .bash instead of .sh because the following command will modify this script
# if it ends in .sh and modifying a script that's currently running causes a tear in the fabric of spacetime

# Remove any windows-specific characters if running in a Windows environment
case "$(uname)" in
   CYGWIN*|MINGW*|MSYS*)
     ./dos2unix.exe *.sh */*.sh
     ;;
esac
docker stack rm In2ItChicago
sleep 5
ENV=${1:-dev}

if [ ! "$(docker network ls | grep in2it)" ]; then
  docker network create --attachable --driver overlay in2it
fi

if [ -f ../ndscheduler/build.sh ]
  ../ndscheduler/build.sh $ENV
fi

./scripts/build-images.sh $ENV
./scripts/check-all-image-updates.sh
./db/run.sh &
./scripts/stack-deploy.sh $ENV