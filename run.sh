#!/bin/bash

export LOG_LEVEL=INFO
export KAFKA_URL="localhost:3000"
export WS_URLS="ws://localhost:10000,ws://localhost:10001"
export PAIR_LIST="BTC/USD,ETH/USD"
set -e
python3 -m src
