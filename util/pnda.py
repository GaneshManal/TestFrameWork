import os
import json
import yaml

import requests



cluster_endpoints = None
edge_ip = None
cluster_reachable = False
proxies = None


def read_cluster_endpoints():
    with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'cluster-conf.yaml') as f:
        user_input = yaml.load(f)

        global edge_ip
        global proxies
        edge_ip = user_input.get("edge_ip")
        dm_port = user_input.get("dm_port", 5000)
        proxies = user_input.get("proxies")

        try:
            response = requests.get("http://%s:%d/environment/endpoints" % (edge_ip, dm_port), proxies=proxies)
            global cluster_reachable
            cluster_reachable = True
        except requests.exceptions.RequestException as e:
            print e
            return

        print "Response Code:", response.status_code
        global cluster_endpoints
        cluster_endpoints = json.loads(response.text)
        print json.dumps(cluster_endpoints)


def read_deployment_manager_endpoint():
    global cluster_endpoints
    if not cluster_endpoints:
        read_cluster_endpoints()
    return edge_ip, 5000, proxies


def read_dataservice_endpoints():
    global cluster_endpoints
    if not cluster_endpoints:
        read_cluster_endpoints()
    return edge_ip, 7000, proxies

