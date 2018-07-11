import nose
# from nose.tools import set_trace; set_trace()
from util.netw_handling import RemoteServer
from util.pnda import ClusterConnection
# from lib.package_repo_manager import PackageRepoManager
from tests.scenario.test_application import TestApplication

def run_tests():
    ClusterConnection().get_cluster_details()


if __name__ == "__main__":
    run_tests()
