import aiohttp
import asyncio
import time
import re
import sys
import logging
from producer_client import KafkaProducerClient
from proto import web_monitor_pb2


class WebMonitor:
    def __init__(
        self, config, config_list, topic, delay, producer=None, regex_pattern=None
    ):
        self.websites = config_list
        self.producer = producer if producer else KafkaProducerClient(config)
        self.topic = topic
        self.delay = delay
        self.running = True
        self.logger = logging.getLogger(__name__)
        self.regex_pattern = regex_pattern
        self.logger.info(f"REGEX PATTERN IS {regex_pattern}")

    async def website_check(self, session, url):
        try:
            async with session.get(url) as resp:
                start_time = asyncio.get_event_loop().time()
                response_body = await resp.text()
                end_time = asyncio.get_event_loop().time()

                response_time = end_time - start_time
                http_status_code = resp.status
                regex_check_result = None

                if self.regex_pattern:
                    regex_check_result = bool(
                        re.search(self.regex_pattern, response_body)
                    )

                http_status_code = resp.status

                # Serialize
                msg = web_monitor_pb2.WebMonitorResult()
                msg.url = url
                msg.succeeded = True
                msg.response_code = http_status_code
                msg.request_time_seconds = response_time

                if regex_check_result:
                    msg.regex_check = regex_check_result

                self.logger.info(
                    f"Sent Msg: url {msg.url}, suceeded {msg.succeeded}, response code  {msg.response_code}, request time {msg.request_time_seconds}, regex_check {regex_check_result}"
                )

                wrapped_msg = msg.SerializeToString()
                self.producer.send_message(self.topic, wrapped_msg)

        except Exception as e:
            self.logger.error(f"Failed fetching {url}: {e}")
            msg = web_monitor_pb2.WebMonitorResult()
            msg.url = url
            msg.succeeded = False
            msg.error.error_message = f"{e}"

            self.logger.info(
                f"Sent: url is {msg.url} succeeded: {msg.succeeded} error msg: {msg.error.error_message}"
            )

            wrapped_msg = msg.SerializeToString()
            self.producer.send_message(self.topic, wrapped_msg)

    async def main(self):
        try:
            while self.running:
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for website in self.websites:
                        url = website["url"]
                        tasks.append(
                            asyncio.ensure_future(self.website_check(session, url))
                        )
                    await asyncio.gather(*tasks)

                await asyncio.sleep(self.delay)
        except KeyboardInterrupt:
            self.stop()
            sys.exit(0)

    def stop(self):
        self.running = False

    def run(self):
        asyncio.run(self.main())
