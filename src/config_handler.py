import json
import re
import logging


class ConfigHandler:
    def __init__(self):
        self.config_list = []
        # Updated regex pattern to match { "url": "foobar" } format
        self.json_list_regex_pattern = '^\{.*"url"\s*:\s*".*"\}$'
        self.kafka_config = None
        self.logger = logging.getLogger(__name__)

    def _open_and_parse_json_file(self, path_to_config):
        try:
            with open(path_to_config, "r") as config_file:
                config_content = config_file.read()
                parsed_json = json.loads(config_content)
            return parsed_json
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {path_to_config}")
            raise e
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in config file: {path_to_config}")
            raise e

    def set_json_config(self, path_to_config):
        try:
            parsed_json = self._open_and_parse_json_file(path_to_config)
            self.logger.info(f"JSON config path set to: {path_to_config}")
            self._convert_json_list_to_dict(parsed_json)
        except Exception as e:
            self.logger.error(f"An error occurred while setting JSON config: {str(e)}")
            raise e

    def set_kafka_config(self, path_to_config):
        try:
            parsed_json = self._open_and_parse_json_file(path_to_config)
            self._convert_kafka_config_to_dict(parsed_json)
        except Exception as e:
            self.logger.error(f"An error occurred while setting Kafka config: {str(e)}")
            raise e

    def _convert_kafka_config_to_dict(self, kafka_json):
        required_keys = [
            "bootstrap_servers",
            "security_protocol",
            "ssl_cafile",
            "ssl_certfile",
            "ssl_keyfile",
        ]

        for key in required_keys:
            if key not in kafka_json:
                self.logger.error(f"Missing '{key}' in the Kafka configuration")
                self.kafka_config = None
                raise ValueError
                return

        self.kafka_config = kafka_json
        self.logger.info(f"Kafka config is set to {self.kafka_config}")

    def _convert_json_list_to_dict(self, parsed_json):
        if isinstance(parsed_json, list):
            for item in parsed_json:
                if re.match(self.json_list_regex_pattern, json.dumps(item)):
                    self.config_list.append(item)
                    self.logger.info(f"Updated config_dict with {item}")
                else:
                    self.logger.error("Invalid dictionary format in JSON list")
                    raise ValueError("Invalid dictionary format in JSON list")
        else:
            self.logger.error("Not a JSON Array - Please check your format")
            self.config_list = None
