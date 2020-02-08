#!/usr/bin/env bash
set -e

./scripts/build-images.sh dev
./scripts/compose-deploy.sh --env dev "$@"
