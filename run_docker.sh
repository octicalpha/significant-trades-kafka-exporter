#!/bin/bash

docker rmi $(docker images | grep stke | awk '{ print $1 }')
docker run --rm --name=stke \
  --network=host \
  -e "LOG_LEVEL=INFO" \
  -e "PAIR_LIST=BTC/USD,ETH/USD" \
  dmi7ry/stke:latest
