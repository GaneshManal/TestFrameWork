import requests
import nose
from util.pynose import skipIf
from util.pnda import ClusterConnection
from util.common import get_logger


class TestDeploymentManager:
    _edge_ip, _dm_port = None, None
    logger = get_logger('TestDeploymentManager')

    def __init__(self):
        self._user = 'pnda'

    @classmethod
    def setup_class(cls):
        cls._edge_ip, cls._dm_port = ClusterConnection().read_deployment_manager_params()

    @skipIf(not ClusterConnection.clusterApiReachable, "cluster Not reachable")
    def test_list_repository_packages(self):
        resp = requests.get("http://%s:%d/repository/packages?user.name=%s" % (self._edge_ip, self._dm_port, self._user))
        nose.tools.eq_(resp.status_code, 200, msg=None)

    @skipIf(not ClusterConnection.clusterApiReachable, "cluster Not reachable")
    def test_list_deployed_packages(self):
        resp = requests.get("http://%s:%d/packages?user.name=%s" % (self._edge_ip, self._dm_port, self._user))
        nose.tools.eq_(resp.status_code, 200, msg=None)
