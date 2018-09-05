#!/bin/bash

export LOG_LEVEL=INFO
export KAFKA_URL="localhost"
export WS_URLS="ws://localhost:3000,ws://localhost:3001"
export PAIR_LIST="BTC/USD,ETH/USD"
set -e
python3 -m src
