# Remove any windows-specific characters if running in a Windows environment
# This script ends in .bash instead of .sh to prevent it from modifying itself and then blowing up
$(dirname $0)/dos2unix.exe *.sh */**.sh