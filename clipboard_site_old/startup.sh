#!/bin/sh
#python3 manage.py runserver 0.0.0.0:8000
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn clipboard.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/usr/src/app/clipboard_site --log-file -