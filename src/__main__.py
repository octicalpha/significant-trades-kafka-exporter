from .settings  import SETTINGS
from .log       import LOGGER
from .classes   import WSListener, TickBuilder, PrintCallback
import asyncio
import functools

if not SETTINGS["kafka_url"]:
    raise Exception("Kafka Url is not defined! App will exit...")
if not SETTINGS["pair_list"]:
    raise Exception("Pair List is not defined! App will exit...")
if len(SETTINGS["ws_urls"]) != len(SETTINGS["pair_list"]):
    raise Exception("Length of pair List doesn't match Length of WS list. App will exit...")

pc = PrintCallback(LOGGER)
workers = []
for i, p in enumerate(SETTINGS["pair_list"]):
    worker = p.copy()
    worker["ws"]        = WSListener(SETTINGS["ws_urls"][i], LOGGER)
    worker["builder"]   = TickBuilder(p["s1"], p["s2"], LOGGER)
    worker["ws"].addCallback(worker["builder"])
    worker["builder"].addCallback(pc)
    workers += [ worker ]
print(workers)

async def run_all_listeners():
    tasks = [
        worker["ws"].run() for worker in workers
    ]
    await asyncio.wait(tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.run_in_executor(None, es.start)
    loop.run_until_complete(run_all_listeners())
