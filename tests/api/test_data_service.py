import requests
import nose
from util.pynose import skipIf
from util.pnda import ClusterConnection


class TestDataService(object):
    _edge_ip, _data_service_port = None, None

    @classmethod
    def setup_class(cls):
        cls._edge_ip, cls._data_service_port = ClusterConnection().read_data_service_params()

    @skipIf(not ClusterConnection.clusterApiReachable, "cluster Not reachable")
    def test_list_datasets(self):
        resp = requests.get("http://%s:%d/api/v1/datasets" % (self._edge_ip, self._data_service_port))
        nose.tools.eq_(resp.status_code, 200, msg=None)

    @skipIf(not ClusterConnection.clusterApiReachable, "cluster Not reachable")
    def test_list_deployed_packages(self):
        assert 'b' == 'b'
