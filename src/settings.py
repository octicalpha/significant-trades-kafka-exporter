import argparse
import os
from .log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--stke_kafka_url",          help="url for kafka",                                   type=str,   default=None)
parser.add_argument("--stke_liquidation_topic",  help="name of topic for liquidation messages",          type=str,   default="liquidations")
parser.add_argument("--stke_trades_topic",       help="name of topic for trading messages",              type=str,   default="trades")
parser.add_argument("--stke_service_topic",      help="name of topic for service messages",              type=str,   default="service")

args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

#override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

LOGGER.warn("starting app with settings: %s" % SETTINGS )
