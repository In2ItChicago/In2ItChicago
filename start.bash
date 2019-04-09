# This file ends in .bash instead of .sh because the following command will modify this script
# if it ends in .sh and modifying a script that's currently running causes a tear in the fabric of spacetime

# Remove any windows-specific characters if running in a Windows environment
case "$(uname)" in
   CYGWIN*|MINGW*|MSYS*)
     ./dos2unix.exe *.sh */*.sh
     ;;
esac
../ndscheduler/build.sh
./scripts/build-images.sh dev
./scripts/check-all-image-updates.sh
docker-compose rm -f -v
./db/run.sh &
./scripts/compose-deploy.sh --env dev "$@"
