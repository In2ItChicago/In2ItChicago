#!/usr/bin/env bash
set -e

scriptpath=$(dirname $0)/check_image_updates.py

echo
echo "============================="
echo "Checking for image updates..."
$scriptpath library/python 3.8 alpine
$scriptpath library/postgres 11.5 alpine
$scriptpath dpage/pgadmin4 4.15
$scriptpath lucaslorentz/caddy-docker-proxy 0.3.3 alpine
$scriptpath library/node 13.2 alpine
$scriptpath portainer/portainer 1.22.2
$scriptpath scrapinghub/splash 3.4
echo "=============================="
echo
