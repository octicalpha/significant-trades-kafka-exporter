from .settings      import SETTINGS
from .log           import LOGGER
from .classes       import WSListener, TickBuilder, PrintCallback, KafkaCallback
from .sts_lookup    import STS_NODES
import asyncio
import functools

if not SETTINGS["kafka_url"]:
    raise Exception("Kafka Url is not defined! App will exit...")

if len(STS_NODES) == 0:
    raise Exception("Cannot find any significant-trades-server nodes on that cluster")

#kafka = KafkaProducer()
topic_mapping = {
    "trade"         : SETTINGS["trades_topic"],
    "liquidation"   : SETTINGS["liquidation_topic"]
}

kafka = KafkaCallback(SETTINGS["kafka_url"],
    type_topic_mapping=topic_mapping,
    default_topic_name=SETTINGS["service_topic"],
    logger=LOGGER
)

workers = []
for node in STS_NODES:
    worker = {}
    worker["ws"]        = WSListener("ws://localhost:" + node["port"], LOGGER)
    worker["builder"]   = TickBuilder(node["s1"], node["s2"], min_export_amount=node["min"], logger=LOGGER)
    worker["ws"].addCallback(worker["builder"])
    worker["builder"].addCallback(kafka)
    workers += [ worker ]
LOGGER.info("Workers: %s" % workers)

async def run_all_listeners():
    tasks = [
        worker["ws"].run() for worker in workers
    ]
    await asyncio.wait(tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.run_in_executor(None, es.start)
    loop.run_until_complete(run_all_listeners())
