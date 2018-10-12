#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi
$pythoncmd -m pip install git+https://github.com/twisted/twisted@992a841506d18a77f8fa15efe4b957e02075a1a1 --upgrade
$pythoncmd -m pip install -r requirements.txt
clipboard_common_lib/install-common-libs.sh
