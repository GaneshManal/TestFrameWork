import requests
import nose
from util.pynose import skip, skipIf
from util.pnda import read_deployment_manager_endpoint, cluster_reachable



class TestDeploymentManager:
    _edge_ip, _dm_port = None, None
    _proxies = None

    def __init__(self):
        self._edge_ip, self._dm_port, self._proxies = read_deployment_manager_endpoint()
        self._user = 'pnda'

    @skipIf(not cluster_reachable, "cluster Not reachable")
    def test_list_repository_packages(self):
        response = requests.get("http://%s:%d/repository/packages?user.name=%s" %
                                (self._edge_ip, self._dm_port, self._user), proxies=proxies)
        print response.text
        nose.tools.eq_(response.status_code, 200, msg=None)

    @skipIf(not cluster_reachable, "cluster Not reachable")
    def test_list_deployed_packages(self):
        response = requests.get("http://%s:%d/packages?user.name=%s" %
                                (self._edge_ip, self._dm_port, self._user), proxies=proxies)
        nose.tools.eq_(response.status_code, 200, msg=None)
