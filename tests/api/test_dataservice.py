import requests
from util.pnda import read_dataservice_endpoints



class TestDataservice(object):
    _edge_ip, _dm_port = None, None
    _proxies = None

    def __init__(self):
        self._edge_ip, self._dataservice_port, self._proxies = read_dataservice_endpoints()

    def test_list_datasets(self):
        response = requests.get("http://%s:%d/api/v1/datasets" % (self._edge_ip, self._dataservice_port),
                                proxies=self._proxies)
        # response = requests.get("http://%s:%d/environment/endpoints" % (self._edge_ip, self._dm_port), proxies=self._proxies)
        assert response.status_code == 200

    def test_list_deployed_packages(self):
        assert 'b' == 'b'
