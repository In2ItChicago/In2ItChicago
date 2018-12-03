# This file ends in .bash instead of .sh because the following command will modify this script
# if it ends in .sh and modifying a script that's currently running causes a tear in the fabric of spacetime

# Remove any windows-specific characters if running in a Windows environment
case "$(uname)" in
   CYGWIN*|MINGW*|MSYS*)
     ./dos2unix.exe *.sh */*.sh
     ;;
esac
ENV=${1:-dev}
./render.sh
./build-images.sh $ENV
./check-all-image-updates.sh
./stack-deploy.sh $ENV