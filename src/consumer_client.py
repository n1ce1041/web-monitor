"""
Consumer Client for testing
"""
from kafka import KafkaConsumer
import proto.web_monitor_pb2 as proto
import json

TOPIC_NAME = "web_monitor"

with open("cfg/kafka.json", "r") as config_file:
    config_content = config_file.read()
    config = json.loads(config_content)


consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=config["bootstrap_servers"],
    client_id="awdawd",
    group_id="awdawd",
    security_protocol=config["security_protocol"],
    ssl_cafile="cfg/ca.pem",
    ssl_certfile="cfg/service.cert",
    ssl_keyfile="cfg/service.key",
)

while True:
    for message in consumer.poll().values():
        for record in message:
            received_data = record.value
            received_msg = proto.WebMonitorResult()
            received_msg.ParseFromString(received_data)

            if received_msg.succeeded:
                print(
                    f" Successful message: url {received_msg.url}, succeeded {received_msg.succeeded} response code = {received_msg.response_code} request time ={received_msg.request_time_seconds}"
                )
            else:
                print(
                    f"Unsuccessful message: url {received_msg.url}, error msg {received_msg.error.error_message}"
                )
