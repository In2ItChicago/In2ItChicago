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
$pythoncmd $scriptpath library/mongo 4.1.7
$pythoncmd $scriptpath library/nginx 1.15.8
$pythoncmd $scriptpath library/node 11.9
$pythoncmd $scriptpath portainer/portainer 1.20.1
echo "=============================="
echo
