#!/usr/bin/env bash
set -e

ssh -nNT -i ~/.ssh/id_rsa -L 3000:127.0.0.1:3000 in2it@104.207.139.250 &
ssh -nNT -i ~/.ssh/id_rsa -L 5000:127.0.0.1:5000 in2it@104.207.139.250 &
ssh -nNT -i ~/.ssh/id_rsa -L 8888:127.0.0.1:8888 in2it@104.207.139.250 &
ssh -nNT -i ~/.ssh/id_rsa -L 5432:/var/run/postgresql/.s.PGSQL.5432 in2it@104.207.139.250 &
ssh -nNT -i ~/.ssh/id_rsa -L 2376:/var/run/docker.sock in2it@104.207.139.250 &
