#!/usr/bin/env bash
set -e

ssh -nNT -i $(dirname $0)/in2it-key.pem -L 3000:localhost:3000 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 5000:localhost:5000 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 8888:localhost:8888 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 6800:localhost:6800 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 5432:localhost:5432 ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 2376:/var/run/docker.sock ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com &
