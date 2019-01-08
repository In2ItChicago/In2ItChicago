scp -v -i ./in2it-key.pem ./deploy.sh ubuntu@ec2-18-221-163-213.us-east-2.compute.amazonaws.com:/home/ubuntu
ssh -v -i ./in2it-key.pem ubuntu@ec2-18-221-163-213.us-east-2.compute.amazonaws.com << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
