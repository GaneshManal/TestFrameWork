import os
import json
import yaml
import requests
from util.common import get_logger


class ClusterConnection:
    clusterApiReachable = False
    cluster_nodes = dict()
    logger = get_logger('ClusterConnection')

    def __init__(self):
        self.endpoints, self.input = dict(), dict()
        with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'user-conf.yaml') as f:
            self.input = yaml.load(f)
        # self.read_cluster_endpoints()

    def read_cluster_endpoints(self):
        edge_node, dm_port = self.input.get('edge_ip'), self.input.get('dm_port', 5000)
        try:
            response = requests.get("http://%s:%d/environment/endpoints" % (edge_node, dm_port))
            ClusterConnection.cluster_reachable = True
        except requests.exceptions.RequestException as e:
            print e
            return
        self.logger.info("Response Code: %d" % response.status_code)
        self.endpoints = json.loads(response.text)

    def read_deployment_manager_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        self.logger.debug('DM params: (Host:%s, Port: %d)' % (self.input.get('edge_ip'), 5000))
        return self.input.get('edge_ip'), 5000

    def read_data_service_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        self.logger.debug('DS params: (Host:%s, Port: %d)' % (self.input.get('edge_ip'), 7000))
        return self.input.get('edge_ip'), 7000

    def read_package_repository_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        self.logger.debug('PRM params: (Host:%s, Port: %d)' % (self.input.get('edge_ip'), 8888))
        return self.input.get('edge_ip'), 8888

    def read_kafka_configuration(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()

        # GAMGAM: Hard Coded
        self.logger.debug('Ganesh actual broker: %s ', self.endpoints.get('kafka_brokers'))
        self.endpoints['kafka_manager'] = 'http://' + self.input.get('kafka_ip') + ':10900/clusters/test-0607'
        self.endpoints['kafka_brokers'] = ':'.join([self.input.get('kafka_ip'), '9092'])
        self.logger.debug('Kafka params: (Manager:%s, Broker: %s)' %
                          (self.endpoints.get('kafka_manager'), self.endpoints.get('kafka_brokers')))
        return self.endpoints.get('kafka_manager'), self.endpoints.get('kafka_brokers')

    def read_hdfs_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        self.logger.debug('HDFS params: (Host:%s, Port: %d)' % (self.input.get('edge_ip'), 8888))
        return self.endpoints.get('webhdfs_host'), self.endpoints.get('webhdfs_port')

    def get_input_applications(self, processing_framework='spark'):
        input_apps = self.input.get('applications').get(processing_framework)
        self.logger.debug('Input Apps: %s' % json.dumps(input_apps))
        return input_apps

    def get_edge_ip(self):
        return self.input.get('edge_ip'), self.input.get('pem_file')

    def exec_command_on_spec_node(self):
        pass
