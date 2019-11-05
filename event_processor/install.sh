#!/bin/sh
if [ "$BUILD_ENV" = "dev" ]
then
    pipenv lock --verbose 
    pipenv install --system --dev --verbose
else
    pipenv install --system --verbose
fi