
until ping -c1 ndscheduler >/dev/null 2>&1; do :; done
# -u is passed to python to return output unbuffered, so there is no delay when viewing docker logs
python -u create_schedules.py
