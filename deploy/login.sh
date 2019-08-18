#!/bin/bash
cat $(dirname $0)/dockerhub_in2itchicago.txt | docker login -u in2itchicago --password-stdin
