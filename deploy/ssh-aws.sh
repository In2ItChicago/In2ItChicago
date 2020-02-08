#!/usr/bin/env bash
set -e

ssh -v -i $(dirname $0)/in2it-key.pem ec2-user@ec2-3-16-31-88.us-east-2.compute.amazonaws.com
