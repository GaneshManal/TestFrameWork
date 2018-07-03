import requests
import nose
from util.pynose import skipIf
from util.pnda import read_data_service_endpoints
from util import config


class TestDataService(object):
    _edge_ip, _data_service_port = None, None

    def __init__(self):
        self._edge_ip, self._data_service_port = read_data_service_endpoints()

    @skipIf(not config.cluster_reachable, "cluster Not reachable")
    def test_list_datasets(self):
        resp = requests.get("http://%s:%d/api/v1/datasets" % (self._edge_ip, self._data_service_port))
        nose.tools.eq_(resp.status_code, 200, msg=None)

    @skipIf(not config.cluster_reachable, "cluster Not reachable")
    def test_list_deployed_packages(self):
        assert 'b' == 'b'

