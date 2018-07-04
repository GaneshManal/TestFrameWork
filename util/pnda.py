import os
import json
import yaml
import requests
import config


def read_cluster_endpoints():
    with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'cluster-conf.yaml') as f:
        user_input = yaml.load(f)

        config.edge_ip = user_input.get("edge_ip")
        dm_port = user_input.get("dm_port", 5000)

        try:
            response = requests.get("http://%s:%d/environment/endpoints" % (config.edge_ip, dm_port))
            config.cluster_reachable = True
        except requests.exceptions.RequestException as e:
            print e
            return
        print "Response Code:", response.status_code
        config.cluster_endpoints = json.loads(response.text)


def read_deployment_manager_endpoint():
    if not config.cluster_endpoints:
        read_cluster_endpoints()
    return config.edge_ip, 5000


def read_data_service_endpoints():
    if not config.cluster_endpoints:
        read_cluster_endpoints()
    return config.edge_ip, 7000


def exec_command_on_spec_node():
    pass
