rm -f twistd.pid
scrapyd & 
rm -rf eggs
rm -rf logs
rm -rf dbs
chmod +x deploy.sh
# -u is passed to python to return output unbuffered, so there is no delay when viewing docker logs
python -u create_schedules.py
sleep 5
scrapyd-deploy