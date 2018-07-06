import os
import json
import yaml
import requests


class ClusterConnection:
    clusterApiReachable = False
    cluster_nodes = dict()

    def __init__(self):
        self.endpoints, self.input = dict(), dict()
        with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'user-conf.yaml') as f:
            self.input = yaml.load(f)

    def read_cluster_endpoints(self):
        edge_node, dm_port = self.input.get('edge_ip'), self.input.get('dm_port', 5000)
        try:
            response = requests.get("http://%s:%d/environment/endpoints" % (edge_node, dm_port))
            ClusterConnection.cluster_reachable = True
        except requests.exceptions.RequestException as e:
            print e
            return
        print "Response Code:", response.status_code
        self.endpoints = json.loads(response.text)

    def read_deployment_manager_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        return self.input.get('edge_ip'), 5000

    def read_data_service_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        return self.input.get('edge_ip'), 7000

    def read_package_repository_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        return self.input.get('edge_ip'), 7000

    def read_kafka_configuration(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        return self.endpoints.get('kafka_manager'), self.endpoints.get('kafka_brokers')

    def read_hdfs_params(self):
        if not ClusterConnection.clusterApiReachable:
            self.read_cluster_endpoints()
        return self.endpoints.get('webhdfs_host'), self.endpoints.get('webhdfs_port')

    def get_input_applications(self, processing_framework='spark'):
        return self.input.get('applications').get(processing_framework)

    def get_edge_ip(self):
        return self.input.get('edge_ip'), self.input.get('pem_file')

    def exec_command_on_spec_node(self):
        pass
