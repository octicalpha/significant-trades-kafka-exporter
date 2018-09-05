#!/bin/bash

docker rmi $(docker images | grep stke)
docker run --rm --name=stke \
  -e "LOG_LEVEL=INFO" \
  -e "KAFKA_URL=localhost:3000" \
  -e "WS_URLS=ws://localhost:10000,ws://localhost:10001" \
  -e "PAIR_LIST=BTC/USD,ETH/USD" \
  dmi7ry/stke:latest
