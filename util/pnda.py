import os
import json
import yaml

import requests

proxies = {
    'http': "socks4://localhost:9999",
    'https': "socks4://localhost:9999"
}

cluster_endpoints = None
edge_ip = None

def read_cluster_endpoints():
    with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'cluster-conf.yaml') as f:
        user_input = yaml.load(f)

        # ip_address = socket.gethostbyname(user_input.get("edge"))
        global edge_ip
        edge_ip = user_input.get("edge_ip")
        dm_port = user_input.get("dm_port", 5000)

        response = requests.get("http://%s:%d/environment/endpoints" % (edge_ip, dm_port), proxies=proxies)
        print "Response Code:", response.status_code

        global cluster_endpoints
        cluster_endpoints = json.loads(response.text)
        print json.dumps(cluster_endpoints)


def read_deployment_manager_endpoint():
    global cluster_endpoints
    if not cluster_endpoints:
        read_cluster_endpoints()
    return edge_ip, 5000



