#!/usr/bin/env bash
set -e

scriptpath=$(dirname $0)/check_image_updates.py

echo
echo "============================="
echo "Checking for image updates..."
$scriptpath library/python 3.8.2 alpine
$scriptpath library/postgres 11.5 alpine
$scriptpath dpage/pgadmin4 4.19
$scriptpath lucaslorentz/caddy-docker-proxy 0.3.6 alpine
$scriptpath library/node 13.10.1 alpine
$scriptpath portainer/portainer 1.23.1
$scriptpath scrapinghub/splash 3.4.1
echo "=============================="
echo
