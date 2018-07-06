import nose
# from nose.tools import set_trace; set_trace()
from util.netw_handling import RemoteServer
from util.pnda import ClusterConnection

def run_tests():
    #nose.main()
    node_ip, pem_file_location = ClusterConnection().get_edge_ip()
    rs = RemoteServer(node_ip, pem_file_location)
    print "making the rs"
    rs.connect()


if __name__ == "__main__":
    run_tests()
