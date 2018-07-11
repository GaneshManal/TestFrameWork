import os
import json
import yaml
import requests
from util.common import get_logger
from util.netw_handling import RemoteServer


class ClusterConnection(object):
    clusterApiReachable = False
    _cluster_nodes = dict()
    _cluster_name = str()
    logger = get_logger('ClusterConnection')

    def __init__(self):
        self.endpoints, self.input = dict(), dict()
        with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'user-conf.yaml') as fd:
            self.input = yaml.load(fd)

    def read_cluster_endpoints(self):
        edge_node, dm_port = self.input.get('edge_ip'), self.input.get('dm_port', 5000)
        try:
            response = requests.get("http://%s:%d/environment/endpoints" % (edge_node, dm_port))
            ClusterConnection.cluster_reachable = True
        except requests.exceptions.RequestException as ex:
            print ex
            return
        self.logger.info("Response Code: %d" % response.status_code)
        self.endpoints = json.loads(response.text)

    def get_cluster_details(self):
        # first get the cluster name
        remote_server = RemoteServer(self.input.get('edge_ip'), self.input.get('pem_file'))
        client = remote_server.connect()
        self.__class__._cluster_name = self.get_cluster_name()
        print "in get all nodes"
        self.__class__._cluster_nodes = remote_server.get_all_nodes(client)
        print self.__class__._cluster_nodes
        remote_server.close_connection(client)

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
        self.endpoints['kafka_manager'] = 'http://' + self.input.get('kafka_ip') \
                                          + ':10900/clusters/' + self.input.get('cluster_name')
        self.endpoints['kafka_brokers'] = ':'.join([self.input.get('kafka_ip'), '9092'])
        self.logger.debug('Kafka params: (Manager:%s, Broker: %s)' %
                          (self.endpoints.get('kafka_manager'),
                           self.endpoints.get('kafka_brokers')))
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
