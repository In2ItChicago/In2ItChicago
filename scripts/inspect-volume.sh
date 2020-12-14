#!/usr/bin/env bash
docker run --rm -i -v=$1:/tmp/$1 busybox find /tmp/$1