ssh -nNT -i $(dirname $0)/in2it-key.pem -L 3000:localhost:3000 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 5000:localhost:5000 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 9000:localhost:9000 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 27017:localhost:27017 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &