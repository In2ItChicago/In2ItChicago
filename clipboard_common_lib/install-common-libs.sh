#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

cd clipboard_common_lib
$pythoncmd setup.py sdist
cd ..
$pythoncmd -m pip install ./clipboard_common_lib