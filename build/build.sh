#!/usr/bin/env zsh

IMAGE_TAG=airflow.dev:local

USER_ID=50000
GROUP_ID=0

docker build -t ${IMAGE_TAG} --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID} -f build/Dockerfile . \
