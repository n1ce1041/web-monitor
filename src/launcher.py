from config_handler import ConfigHandler
from producer_client import KafkaProducerClient
from web_monitor import WebMonitor
import argparse
import asyncio
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_format = "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(log_format, datefmt=date_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def launcher():
    parser = argparse.ArgumentParser(description="Web Monitor")

    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="Kafka topic name",
    )

    parser.add_argument(
        "--regex",
        type=str,
        required=False,
        default=None,
        help="regex pattern to check response bodies against",
    )

    parser.add_argument(
        "--delay",
        type=int,
        default=300,
        help="Delay in seconds between website checks (default: 300)",
    )

    args = parser.parse_args()

    # Launch cfg and pass to webmonitor
    config_handler = ConfigHandler()
    config_handler.set_json_config("./cfg/config.json")
    config_handler.set_kafka_config("./cfg/kafka.json")

    web_monitor = WebMonitor(
        config=config_handler.kafka_config,
        config_list=config_handler.config_list,
        topic=args.topic,
        delay=args.delay,
        regex_pattern=args.regex,
    )

    sys.exit(web_monitor.run())


if __name__ == "__main__":
    launcher()
