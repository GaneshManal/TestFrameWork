import nose
from util.pnda import read_cluster_endpoints
from tests.api.test_data_service import TestDataService


def run_tests():

    cluster_config = read_cluster_endpoints()
    print cluster_config
    ds_obj = TestDataService()
    ds_obj.test_list_datasets()

    nose.main()


if __name__ == "__main__":
    run_tests()
