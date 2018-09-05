from .callback import Callback
from .tick import Tick
import asyncio

class PrintCallback(Callback):

    def __init__(self, logger=None):
        super().__init__("PrintCallback", logger=logger)

    async def processCallback(self, obj):
        print (str(obj))
