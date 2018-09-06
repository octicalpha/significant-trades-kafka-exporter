#!/bin/bash

export LOG_LEVEL=INFO
export KAFKA_URL="localhost:3000"
set -e
python3 -m src
