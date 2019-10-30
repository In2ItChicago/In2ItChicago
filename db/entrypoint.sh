#!/bin/sh
#until ping -c1 postgres >/dev/null 2>&1; do :; done
cd /usr/src
python deploy.py $1