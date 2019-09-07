if [ "$RUN_SCHEDULER" = "1" ]
then
    rm -f twistd.pid
    scrapyd & 
    rm -rf eggs
    rm -rf logs
    rm -rf dbs
    until ping -c1 ndscheduler >/dev/null 2>&1; do :; done
    # -u is passed to python to return output unbuffered, so there is no delay when viewing docker logs
    python -u create_schedules.py 
    sleep 5
    scrapyd-deploy
    while true; do sleep 10000; done
else
    python -u runner.py
fi