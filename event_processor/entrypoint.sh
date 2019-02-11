rm -f twistd.pid
scrapyd & 
rm -rf eggs
rm -rf logs
rm -rf dbs
chmod +x deploy.sh
sleep 5
./node_modules/nodemon/bin/nodemon.js -L --exec ./deploy.sh