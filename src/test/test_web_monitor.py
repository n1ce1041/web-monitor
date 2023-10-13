import pytest
from unittest.mock import MagicMock, patch
from web_monitor import WebMonitor


@pytest.fixture
def web_monitor(mocker):
    config = {
        "bootstrap_servers": "kafka_server",
        "security_protocol": "PLAINTEXT",
        "ssl_cafile": "/path/to/cafile",
        "ssl_certfile": "/path/to/certfile",
        "ssl_keyfile": "/path/to/keyfile",
    }
    websites = [
        {"url": "https://google.com", "regex_pattern": ""},
        {"url": "https://example.com", "regex_pattern": ""},
    ]
    producer_client = mocker.MagicMock()
    return WebMonitor(config, websites, "test_topic", 1, producer=producer_client)


@pytest.mark.asyncio
async def test_website_check_success(web_monitor, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status = 200
    mock_response.text.return_value = "Mocked response"

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        await web_monitor.website_check(None, "https://example.com")

    web_monitor.producer.send_message.assert_called_once_with("test_topic", mocker.ANY)


@pytest.mark.asyncio
async def test_website_check_failure(web_monitor, mocker):
    mock_response = mocker.MagicMock()
    mock_response.status = 404

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        await web_monitor.website_check(None, "https://example.com")

    web_monitor.producer.send_message.assert_called_once_with("test_topic", mocker.ANY)


def test_stop(web_monitor):
    assert web_monitor.running is True
    web_monitor.stop()
    assert web_monitor.running is False
