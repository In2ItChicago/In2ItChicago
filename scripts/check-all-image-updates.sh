#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

scriptpath=$(dirname $0)/check_image_updates.py

echo
echo "============================="
echo "Checking for image updates..."
$pythoncmd $scriptpath library/python 3.7.2
$pythoncmd $scriptpath library/mongo 4.1.9
$pythoncmd $scriptpath library/nginx 1.15.9
$pythoncmd $scriptpath library/node 11.11
$pythoncmd $scriptpath portainer/portainer 1.20.2
echo "=============================="
echo
