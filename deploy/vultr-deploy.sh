#!/usr/bin/env bash
set -e

scp -v -i ~/.ssh/id_rsa $(dirname $0)/deploy.sh in2it@104.207.139.250:/home/in2it
scp -v -i ~/.ssh/id_rsa $(dirname $0)/../.env-prod in2it@104.207.139.250:/home/in2it/In2ItChicago
scp -v -i ~/.ssh/id_rsa $(dirname $0)/../caddy/caddy-private.pem in2it@104.207.139.250:/home/in2it/In2ItChicago/caddy
scp -v -i ~/.ssh/id_rsa $(dirname $0)/../caddy/caddy-public.pem in2it@104.207.139.250:/home/in2it/In2ItChicago/caddy
ssh -v -i ~/.ssh/id_rsa in2it@104.207.139.250  << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
