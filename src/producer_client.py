import json
import logging
from kafka import KafkaProducer


class KafkaProducerClient:
    def __init__(self, config):
        self.config_dict = config
        self.producer = None
        self.logger = logging.getLogger(__name__)
        self._initialize_producer()

    def _initialize_producer(self):
        if self.config_dict is None:
            raise ValueError("No Config Present - Config Not Set")

        self.producer = KafkaProducer(
            bootstrap_servers=self.config_dict.get("bootstrap_servers"),
            security_protocol=self.config_dict.get("security_protocol"),
            ssl_cafile=self.config_dict.get("ssl_cafile"),
            ssl_certfile=self.config_dict.get("ssl_certfile"),
            ssl_keyfile=self.config_dict.get("ssl_keyfile"),
        )
        self.logger.info("Kafka producer initialized")

    def send_message(self, topic, message):
        if self.producer is None:
            self._initialize_producer()

        if not isinstance(message, bytes):
            self.logger.error("Message must be bytes")
            raise ValueError("Message must be bytes")

        self.producer.send(topic, value=message)
        self.logger.info(f"Message sent to topic '{topic}'")

    def close(self):
        if self.producer is not None:
            self.producer.close()
            self.logger.info("Kafka producer closed")
