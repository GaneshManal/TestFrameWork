import requests


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

    def _run_producer(self, topic, event_count, producer_type):
        is_successfully_produced = False
        produced_count = eval("%s_producer.produce(self.kafka_broker, topic, event_count)" % producer_type)
        if produced_count == event_count:
            is_successfully_produced = True
        return is_successfully_produced

    def run_producer(self, package, topic, event_count):
        producer_result = self._run_producer(topic, event_count, "sb")
        return producer_result
