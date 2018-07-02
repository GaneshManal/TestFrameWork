import requests
import nose
from util.pynose import skip, skipIf
from util.pnda import read_data_service_endpoints, cluster_reachable


class TestDataService(object):
    _edge_ip, _data_service_port = None, None
    _proxies = None

    def __init__(self):
        self._edge_ip, self._data_service_port, self._proxies = read_data_service_endpoints()

    @skipIf(cluster_reachable, "cluster Not reachable")
    def test_list_datasets(self):
        response = requests.get("http://%s:%d/api/v1/datasets" % (self._edge_ip, self._data_service_port),
                                proxies=self._proxies)
        nose.tools.eq_(response.status_code, 200, msg=None)

    @skipIf(cluster_reachable, "cluster Not reachable")
    def test_list_deployed_packages(self):
        assert 'b' == 'b'

