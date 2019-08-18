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
$pythoncmd $scriptpath library/python 3.7.3 alpine
$pythoncmd $scriptpath library/postgres 11.5 alpine
$pythoncmd $scriptpath dpage/pgadmin4 4.11
$pythoncmd $scriptpath library/nginx 1.17.3 alpine
$pythoncmd $scriptpath library/nginx 1.17.3
$pythoncmd $scriptpath library/node 12.8.1 alpine
$pythoncmd $scriptpath portainer/portainer 1.22.0
echo "=============================="
echo
