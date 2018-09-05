import argparse
import os
from .log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--ws_urls",            help="ws:// or wss:// url to listen (comma separated)", type=str,   default="ws://localhost:3000")
parser.add_argument("--pair_list",          help="trading pair list (comma separated)",             type=str,   default=None)
parser.add_argument("--kafka_url",          help="url for kafka",                                   type=str,   default=None)
parser.add_argument("--liquidation_topic",  help="name of topic for liquidation messages",          type=str,   default="liquidations")
parser.add_argument("--trades_topic",       help="name of topic for trading messages",              type=str,   default="trades")
parser.add_argument("--service_topic",      help="name of topic for service messages",              type=str,   default="service")

args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

#override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

if SETTINGS["ws_urls"]:
    SETTINGS["ws_urls"] = SETTINGS["ws_urls"].split(",")
if SETTINGS["pair_list"]:
    pair_list = SETTINGS["pair_list"].upper().split(",")
    new_pair_list = []
    for pair in pair_list:
        if "/" not in pair:
            raise Exception("Pair %s must contain separator '/'!")
        spl = pair.split("/")
        new_pair_list.append({ "s1": spl[0], "s2": spl[1], "pair": pair.lower().replace("/", "") })
    SETTINGS["pair_list"] = new_pair_list

LOGGER.warn("starting app with settings: %s" % SETTINGS )
