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
$pythoncmd $scriptpath python 3.7.2
$pythoncmd $scriptpath mongo 4.1.6
$pythoncmd $scriptpath nginx 1.15.8
$pythoncmd $scriptpath node 11.6
echo "=============================="
echo
