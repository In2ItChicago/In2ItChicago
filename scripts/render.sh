#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

$pythoncmd $(dirname "$0")/render.py nginx/nginx.conf.j2