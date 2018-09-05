import websockets
import asyncio
from .callback import Callback
from kafka import KafkaProducer
from kafka.errors import KafkaError

class KafkaProducer(Callback):

    kafka_url           = ""
    producer            = None
    type_topic_mapping  = None
    default_topic_name  = None
    default_retries     = None

    def __init__(self, kafka_url="", logger=None, type_topic_mapping=[], default_topic_name="other", default_retries=3):
        super().__init__("KafkaProducer", logger=logger)

        self.kafka_url          = ws_url
        self.type_topic_mapping = type_topic_mapping
        self.default_topic_name = default_topic_name
        self.default_retries    = default_retries

        self.init()

    def init(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=["kafka_url"],
                value_serializer=lambda m: json.dumps(m).encode('ascii'),
                retries=3
            )
        except Exception as e:
            self.logger.exception("Error during kafka connection! %s" % e)

    def processCallback(self, obj):
        selected_topic = self.default_topic_name
        message_type = obj.get("type", None)
        if message_type and message_type in self.type_topic_mapping:
            selected_topic = self.type_topic_mapping[message_type]

        if type(obj) != dict:
            raise Exception("object %s is not a dict!" % s)

        self.producer.send(selected_topic, obj).add_callback(_kafka_log_success).add_errback(_kafka_log_error)

    def _kafka_log_success(self, message):
        self.logger.info(message)

    def _kafka_log_error(self, message):
        self.logger.warning(message)
