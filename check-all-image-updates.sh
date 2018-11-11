#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

echo
echo "============================="
echo "Checking for image updates..."
$pythoncmd check_image_updates.py python 3.7
$pythoncmd check_image_updates.py mongo 4.1.4
$pythoncmd check_image_updates.py nginx 1.15.5
$pythoncmd check_image_updates.py node 8.12.0
echo "=============================="
echo
