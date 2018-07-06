import requests
import os
import io
import time
import json
import avro.schema
import avro.io
from kafka import KafkaProducer
from util.common import get_logger


class KafkaManager(object):
    logger = get_logger('KafkaManager')

    def __init__(self, manager, broker):
        self.manager = manager
        self.broker = broker
        self.logger.info('Manager: %s, broker: %s' % (self.manager, self.broker))

    def create_topic(self, topic_name, partition_count=1, replica_factor=1):
        self.logger.info('Creating Kafka Topic - %s', topic_name)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"topic": "%s" % topic_name, "partitions": "%d" % partition_count, "replication": "%d" % replica_factor}
        url = "%s/topics/create" % self.manager
        self.logger.debug('url - %s, data - %s' % (url, json.dumps(data)))

        res = requests.post(url, data=data, headers=headers)
        self.logger.debug('response - %d', res.status_code)
        if res.status_code == 200:
            return True
        return False

    def delete_topic(self, topic_name):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"topic": "%s" % topic_name}
        uri = "%s/topics/delete" % self.manager

        res = requests.post(uri, data=data, headers=headers)
        if res.status_code == 200:
            return True
        return False

    def run_producer(self, app_details):
        self.logger.debug('Ganesh - inside run producer')
        produced_count = self._produce_data(app_details)
        if produced_count == app_details.get('event-count'):
            return True
        return False

    def _produce_data(self, app_details):
        producer = KafkaProducer(bootstrap_servers=[self.broker], api_version=(0, 10, 1))

        # Load AVRO schema
        schema_file = os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'dataplatform-raw.avsc'
        schema = avro.schema.parse(open(schema_file).read())
        current_milli_time = lambda: int(round(time.time() * 1000))

        count = 0
        while count < app_details.get('event-count', 10):
            writer = avro.io.DatumWriter(schema)
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)

            self.logger.debug('Writing rawdata: %s', '"a=1;b=2;')
            writer.write({"source": app_details.get('name'), "timestamp": current_milli_time(),
                          "rawdata": "a=1;b=2;c=%s;gen_ts=%s" % (count, current_milli_time())}, encoder)
            raw_bytes = bytes_writer.getvalue()
            producer.send(app_details.get('topic-name'), raw_bytes)
            count += 1

        self.logger.info('Data produced successfully')
        producer.close()
        return count
