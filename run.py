import nose
# from nose.tools import set_trace; set_trace()
from util.netw_handling import RemoteServer
from util.pnda import ClusterConnection
# from lib.package_repo_manager import PackageRepoManager
from tests.scenario.test_application import TestApplication

def run_tests():
    #nose.main()
    node_ip, pem_file_location = ClusterConnection().get_edge_ip()
    rs = RemoteServer(node_ip, pem_file_location)
    print "making the rs"
    rs.connect()
    # nose.main()
    # url = "https://s3.amazonaws.com/pnda-apps-public/spark-batch-example-app-wf-1.1.2.tar.gz"
    # ret = PackageRepoManager.download_network_package(url)

    app_obj = TestApplication()
    app_obj.setup_class()
    app_obj.test_spark_applications()


if __name__ == "__main__":
    run_tests()
