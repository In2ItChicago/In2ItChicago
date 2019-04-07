scp -v -i $(dirname $0)/in2it-key.pem $(dirname $0)/deploy.sh ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com:/home/ec2-user
ssh -v -i $(dirname $0)/in2it-key.pem ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com << EOF
chmod +x ~/deploy.sh
~/deploy.sh
EOF
