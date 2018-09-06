#!/bin/bash

docker rmi $(docker images | grep stke | awk '{ print $1 }')
docker run --rm \
  --name=stke \
  --network=host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e "LOG_LEVEL=INFO" \
  -e "KAFKA_URL=localhost:9092" \
  dmi7ry/stke:latest
