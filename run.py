import os
import yaml
from util.pnda import PndaCluster


def run_tests():

    with open(os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'cluster-conf.yaml') as f:
        user_input = yaml.load(f)

    cluster_obj = PndaCluster(user_input.get('edge'))
    cluster_obj.read_cluster_config()
    print cluster_obj


if __name__ == "__main__":
    run_tests()
