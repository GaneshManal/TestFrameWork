import requests
import os
import io
import time
import avro.schema
import avro.io
from kafka import KafkaProducer


class KafkaManager(object):

    def __init__(self, manager, broker):
        self.manager = manager
        self.broker = broker

    def create_topic(self, topic_name, partition_count=1, replica_factor=1):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"topic": "%s" % topic_name, "partitions": "%d" % partition_count, "replication": "%d" % replica_factor}
        uri = "%s/topics/create" % self.manager

        res = requests.post(uri, data=data, headers=headers)
        if res.status_code == 200:
            return True
        return False

    def run_producer(self, app_details):
        produced_count = self._produce_data(app_details)
        if produced_count == app_details.get('event-count'):
            return True
        return False

    def _produce_data(self, app_details):
        producer = KafkaProducer(bootstrap_servers=self.broker)

        # Load AVRO schema
        schema_file = os.getcwd() + os.pathsep + 'conf' + os.pathsep + 'dataplatform-raw.avsc'
        schema = avro.schema.parse(open(schema_file).read())
        current_milli_time = lambda: int(round(time.time() * 1000))

        seq = 0
        while seq < app_details.get('event-count', 10):
            writer = avro.io.DatumWriter(schema)
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            writer.write({"source": app_details.get('name'), "timestamp": current_milli_time(),
                          "rawdata": "a=1;b=2;c=%s;gen_ts=%s" % (seq, current_milli_time())}, encoder)
            raw_bytes = bytes_writer.getvalue()
            producer.send(app_details.get('topic-name'), raw_bytes)
            seq += 1

        producer.close()
        return seq
