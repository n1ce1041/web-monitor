import os
import pytest
import json
from unittest.mock import mock_open, patch
from config_handler import ConfigHandler


@pytest.fixture
def config_handler():
    return ConfigHandler()


def test_set_json_config_valid_json(config_handler, tmp_path):
    config_path = tmp_path / "config.json"
    config_data = '[{"url": "http://example.com", "regex_pattern": ".*"}]'
    with open(config_path, "w") as config_file:
        config_file.write(config_data)

    config_handler.set_json_config(config_path)

    assert config_handler.config_list == [
        {"url": "http://example.com", "regex_pattern": ".*"}
    ]


def test_set_json_config_file_not_found(config_handler):
    with pytest.raises(FileNotFoundError):
        config_handler.set_json_config("non_existent_file.json")


def test_set_json_config_invalid_json(config_handler, tmp_path):
    config_path = tmp_path / "config.json"
    invalid_config_data = (
        '{"url": "http://example.com", "regex_pattern": ".*",}'  # Trailing comma
    )

    with open(config_path, "w") as config_file:
        config_file.write(invalid_config_data)

    with pytest.raises(json.JSONDecodeError):
        config_handler.set_json_config(config_path)


def test_convert_json_list_to_dict_valid_format(config_handler):
    json_list = '[{"url": "http://example.com", "regex_pattern": ".*"}]'

    config_handler._convert_json_list_to_dict(json.loads(json_list))

    assert config_handler.config_list == [
        {"url": "http://example.com", "regex_pattern": ".*"}
    ]


def test_convert_json_list_to_dict_invalid_format(config_handler):
    invalid_json_list = '[{"url": "http://example.com", "regex_pattern": ".*",}]'  # Trailing comma to make it invalid

    config_handler._convert_json_list_to_dict(invalid_json_list)
    assert config_handler.config_list == None


def test_convert_json_list_to_dict_invalid_dict_format(config_handler):
    invalid_json_list = '[{"invalid_key": "value"}]'

    config_handler._convert_json_list_to_dict(invalid_json_list)
    assert config_handler.config_list == None


def test_convert_json_list_to_dict_non_list_input(config_handler):
    non_list_json = '{"url": "http://example.com", "regex_pattern": ".*"}'

    config_handler._convert_json_list_to_dict(non_list_json)
    assert config_handler.config_list == None


def test_set_valid_kafka_config(tmpdir):
    config_path = tmpdir.join("valid_kafka_config.json")
    valid_config_data = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    with open(config_path, "w") as config_file:
        json.dump(valid_config_data, config_file)

    config_handler = ConfigHandler()
    config_handler.set_kafka_config(config_path)

    assert config_handler.kafka_config == valid_config_data


def test_valid_json_but_missing_key_kafka_config(tmpdir):
    config_path = tmpdir.join("valid_json_missing_key.json")
    invalid_config_data = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        # Missing ssl_certfile key
        "ssl_keyfile": "/path/to/keyfile",
    }
    with open(config_path, "w") as config_file:
        json.dump(invalid_config_data, config_file)

    config_handler = ConfigHandler()

    with pytest.raises(ValueError):
        config_handler.set_kafka_config(config_path)


def test_invalid_json_kafka_config(tmpdir):
    config_path = tmpdir.join("invalid_json.json")
    invalid_json_data = "this is not valid JSON"
    with open(config_path, "w") as config_file:
        config_file.write(invalid_json_data)

    config_handler = ConfigHandler()

    with pytest.raises(json.JSONDecodeError):
        config_handler.set_kafka_config(config_path)
