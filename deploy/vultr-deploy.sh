#!/usr/bin/env bash
set -e

scp -v -i ~/.ssh/id_rsa $(dirname $0)/deploy.sh in2it@104.207.139.250:/home/in2it
scp -v -i ~/.ssh/id_rsa $(dirname $0)/../.env-prod in2it@104.207.139.250:/home/in2it/In2ItChicago
ssh -v -i ~/.ssh/id_rsa in2it@104.207.139.250  << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
