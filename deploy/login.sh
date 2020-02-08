#!/usr/bin/env bash
set -e

cat $(dirname $0)/dockerhub_in2itchicago.txt | docker login -u in2itchicago --password-stdin
