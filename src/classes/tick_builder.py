import json
import asyncio
import functools
from .callback import Callback
from .tick import Tick


class TickBuilder(Callback):

    symbol1             = None
    symbol2             = None
    min_export_amount   = 0

    def __init__(self, symbol1, symbol2, logger=None, min_export_amount=0):
        super().__init__("TickBuilder", objectType=Tick, logger=logger)
        self.symbol1 = symbol1.lower()
        self.symbol2 = symbol2.lower()
        self.min_export_amount = min_export_amount
        self.logger.warn("Started TickBuilder: %s/%s MIN_AMOUNT=%s" % ( self.symbol1, self.symbol2, self.min_export_amount ))

    def _parseMessage(self, message):
        parsed = None
        if type(message) is str:
            parsed = json.loads(message)
        elif type(message) is list:
            parsed = message
        else:
            raise Exception("message: type(%s) = %s is not a list or cannot be parsed" % ( message, type(message) ))
        return parsed

    def _processMessage(self, message):
        try:
            parsed_message = self._parseMessage(message)
        except Exception as e:
            self.logger.exception("Error during _parseMessage: %s" % e)
            return

        exchange           = parsed_message[0]
        timestamp          = int(parsed_message[1])
        price              = float(parsed_message[2])
        amount             = float(parsed_message[3])
        deal               = "short" if parsed_message[4] == 0 else "long"
        type               = "trade" if len(parsed_message) == 5 else "liquidation"

        if len(parsed_message) not in (5,6):
            self.logger.warn("Unsupported message length: %s" % message)
        valid = True

        if valid is True and amount >= self.min_export_amount:
            return Tick(exchange, timestamp, price, amount, deal, self.symbol1, self.symbol2, type)

    def _processMessageList(self, messageList):
        try:
            if type(messageList) is str:
                messageList = json.loads(messageList)
        except Exception as e:
            self.logger.exception("MessageList=%s cannot be parsed!" % messageList)
        if type(messageList) is list:
            yield from (self._processMessage(message) for message in messageList if self._processMessage(message) is not None)
        elif type(messageList) is dict:
            service_message = messageList.copy()
            service_message["pair"] = self.symbol1 + self.symbol2
            if obj.get("type", None):
                obj["message_type"] = obj["type"]
                obj["type"] = "service"
            return [ service_message ]
        else:
            self.logger.exception("%s: %s is not a list" % ( self.name, messageList ))

    async def callback(self, obj):
        try:
            tasks = [
                asyncio.ensure_future(cb.callback(processResult))
                for cb in self.callbackList
                for processResult in self._processMessageList(obj)
            ]
            if len(tasks) != 0:
                await asyncio.wait(tasks)
        except Exception as e:
            self.logger.exception("Exception during callback: %s" % e)
