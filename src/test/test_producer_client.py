import unittest
import pytest
from unittest.mock import MagicMock, patch
from producer_client import KafkaProducerClient


@patch("producer_client.logging")
@patch("producer_client.KafkaProducer")
def test_initialize_producer(mock_kafka_producer, mock_logging):
    config = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    client = KafkaProducerClient(config)

    assert client.config_dict == config
    assert client.producer is not None
    mock_kafka_producer.assert_called_once_with(
        bootstrap_servers=config["bootstrap_servers"],
        security_protocol=config["security_protocol"],
        ssl_cafile=config["ssl_cafile"],
        ssl_certfile=config["ssl_certfile"],
        ssl_keyfile=config["ssl_keyfile"],
    )
    mock_logging.getLogger.assert_called_once_with("producer_client")


@patch("producer_client.logging")
@patch("producer_client.KafkaProducer")
def test_send_message(mock_kafka_producer, mock_logging):
    config = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    client = KafkaProducerClient(config)

    mock_producer_instance = mock_kafka_producer.return_value
    mock_producer_instance.send.return_value = MagicMock()

    topic = "test_topic"
    message = b"test_message"

    client.send_message(topic, message)

    mock_producer_instance.send.assert_called_once_with(topic, value=message)
    mock_logging.getLogger.assert_called_once_with("producer_client")
    mock_logging.getLogger.return_value.error.assert_not_called()


@patch("producer_client.logging")
@patch("producer_client.KafkaProducer")
def test_send_message_invalid_message_type(mock_kafka_producer, mock_logging):
    config = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    client = KafkaProducerClient(config)

    mock_producer_instance = mock_kafka_producer.return_value
    mock_producer_instance.send.return_value = MagicMock()

    topic = "test_topic"
    message = "test_message"  # Not bytes, should raise an error

    with pytest.raises(ValueError):
        client.send_message(topic, message)

    mock_producer_instance.send.assert_not_called()
    mock_logging.getLogger.assert_called_once_with("producer_client")
    mock_logging.getLogger.return_value.error.assert_called_once()


@patch("producer_client.logging")
@patch("producer_client.KafkaProducer")
def test_close(mock_kafka_producer, mock_logging):
    config = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    client = KafkaProducerClient(config)

    mock_producer_instance = mock_kafka_producer.return_value
    client.close()

    mock_producer_instance.close.assert_called_once()
    mock_logging.getLogger.assert_called_once_with("producer_client")
