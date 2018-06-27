import requests
import json

proxies = {
    'http': "socks4://localhost:9999",
    'https': "socks4://localhost:9999"
}


class PndaCluster:
    _edge_ip = None
    _dm_port = None
    _endpoints = None

    def __init__(self, edge_ip, dm_port=5000):
        self._edge_ip = edge_ip
        self._dm_port = dm_port

    def is_reachable(self):
        pass

    def read_cluster_nodes(self):
        pass

    def read_cluster_config(self):
        response = requests.get("http://%s:%d/environment/endpoints" % (self._edge_ip, self._dm_port), proxies=proxies)
        print "Response Code:", response.status_code
        self._endpoints = json.loads(response.text)

