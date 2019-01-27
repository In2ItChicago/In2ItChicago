#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

$pythoncmd -m pip install -r requirements.txt
docker network create in2it
