ssh -nNT -i $(dirname $0)/in2it-key.pem -L 3000:localhost:3000 ubuntu@3.17.64.55 &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 5000:localhost:5000 ubuntu@3.17.64.55 &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 9000:localhost:9000 ubuntu@3.17.64.55 &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 27017:localhost:27017 ubuntu@3.17.64.55 &
ssh -nNT -i $(dirname $0)/in2it-key.pem -L 80:localhost:80 ubuntu@3.17.64.55 &