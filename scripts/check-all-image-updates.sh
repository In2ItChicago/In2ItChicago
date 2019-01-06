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
$pythoncmd $scriptpath python 3.7.1
$pythoncmd $scriptpath mongo 4.1.5
$pythoncmd $scriptpath nginx 1.15.7
$pythoncmd $scriptpath node 11.3
echo "=============================="
echo
