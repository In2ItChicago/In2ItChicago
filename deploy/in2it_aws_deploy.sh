scp -v -i ./in2it-key.pem ./deploy.sh ubuntu@3.17.64.55:/home/ubuntu
ssh -v -i ./in2it-key.pem ubuntu@3.17.64.55 << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
