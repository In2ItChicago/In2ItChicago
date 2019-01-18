$(dirname $0)/publish-images.sh
scp -v -i $(dirname $0)/in2it-key.pem $(dirname $0)/deploy.sh ubuntu@3.17.64.55:/home/ubuntu
ssh -v -i $(dirname $0)/in2it-key.pem ubuntu@3.17.64.55 << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
