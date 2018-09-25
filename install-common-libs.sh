#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
	pipcmd=pip3
else
	pythoncmd=python
	pipcmd=pip
fi

cd clipboard_common_lib
$pythoncmd setup.py sdist
cd ..
$pipcmd install ./clipboard_common_lib