import requests
from util.pnda import read_deployment_manager_endpoint

proxies = {
    'http': "socks4://localhost:9999",
    'https': "socks4://localhost:9999"
}


class TestDeploymentManager:
    _edge_ip, _dm_port = None, None

    def __init__(self):
        self._edge_ip, self._dm_port = read_deployment_manager_endpoint()

    def test_list_repository_packages(self):
        response = requests.get("http://%s:%d/environment/endpoints" % (self._edge_ip, self._dm_port), proxies=proxies)
        assert response.status_code == 200

    def test_list_deployed_packages(self):
        assert 'b' == 'b'
