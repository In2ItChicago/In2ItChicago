#!/bin/bash

./scripts/build-images.sh dev
./scripts/compose-deploy.sh --env dev "$@"
