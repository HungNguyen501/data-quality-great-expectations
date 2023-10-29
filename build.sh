#!/usr/bin/env zsh

IMAGE_TAG=airflow.dev:local

USER_ID=50000
GROUP_ID=0

docker build -t ${IMAGE_TAG} --build-arg user_id=${USER_ID} --build-arg group_id=${GROUP_ID} .
