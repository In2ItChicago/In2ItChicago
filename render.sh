#!/bin/bash
if command -v python3 &>/dev/null; then
	pythoncmd=python3
else
	pythoncmd=python
fi

$pythoncmd render.py nginx/nginx.conf.j2