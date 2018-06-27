import json
import requests


class PndaCluster:
    _edge_ip = None
    _dm_port = None

    def __init__(self, edge_ip, dm_port=5000):
        self._edge_ip = edge_ip
        self._dm_port = dm_port

    def is_reachable(self):
        pass

    def read_cluster_nodes(self):
        pass

    def read_cluster_services(self):

        res = requests.get("http://%s:%d/environment/endpoints" % (self._edge_ip, self._dm_port))
        print json.dumps(res)

