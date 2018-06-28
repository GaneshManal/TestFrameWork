import os
import yaml
from util.pnda import PndaCluster


def run_tests():

    cluster_obj = PndaCluster()
    cluster_obj.read_cluster_config()
    # print cluster_obj


if __name__ == "__main__":
    run_tests()
