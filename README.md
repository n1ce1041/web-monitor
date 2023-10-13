## About

Web monitor asynchronously checks websites periodically and sends the status of given websites via protobuf serialized messages to an Aiven Kafka Instance.

## Getting Started

### Prerequisites

Web monitor requires protoc in order to compile web_monitor.proto and serialize/deserialize messages.

### Build and test

From the project root, simply run ./devstart.sh to create a venv and install all dependencies.

To run all tests , from the project root inside a terminal run 

```pytest```

### Config

Place your relevant certificates and keys(ca.pem , service.cert , service.key) for your Aiven Kafka instance inside src/cfg. 

src/config.json also contains a json array of websites in the format

```[ { "url": "foobar "}]```

Simply add your url object and keys to this array for websites you wish to monitor.

src/kafka.json contains a json object that has the keys already configured, simply add the relevant values for your Aiven Kafka instance.

### Run
Ensure your venv is activated with 

```source venv/bin/activate```

From the project root move into the src folder with

```cd src/```


To run the web monitor application:

```python3 launcher.py --topic web_monitor --delay 300 --regex ".*"```

Modify --topic to a topic relevant to your needs. --delay is period of time in seconds between each cycle of website monitoring. --regex checks response bodies of websites against the pattern of your specification. Please be aware that your pattern needs to be within quotes(double or single) to be parsed correctly.

To run a test consumer with the web monitor application, open another terminal instance:

```cd src;```
```python3 consumer_client.py```