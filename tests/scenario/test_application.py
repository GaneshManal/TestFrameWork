from nose import with_setup

from util.pnda import ClusterConnection
from lib.kafka_manager import KafkaManager
from lib.deployment_manager import DeploymentManager
from lib.package_repo_manager import PackageRepoManager
from lib.hdfs_manager import HDFSManager


class TestApplication(object):
    _deployment_manager, _package_repo_manager = None, None
    _kafka_manager, _hdfs_manager = None, None

    _spark_apps = dict()
    _conn_obj = None

    @classmethod
    def setup_class(cls):
        cls._conn_obj = ClusterConnection()

        kafka_manager, kafka_broker = cls._conn_obj.read_kafka_configuration()
        cls._kafka_manager = KafkaManager(kafka_manager, kafka_broker)

        dm_host, dm_port = cls._conn_obj.read_deployment_manager_params()
        cls._deployment_manager = DeploymentManager(dm_host, dm_port)

        prm_host, prm_port = cls._conn_obj.read_package_repository_params()
        cls._package_repo_manager = PackageRepoManager(prm_host, prm_host)

        hdfs_host, hdfs_port = cls._conn_obj.read_hdfs_params()
        cls._hdfs_manager = HDFSManager(hdfs_host, hdfs_port)

    def set_spark_app(self):
        self._spark_apps = self._conn_obj.get_input_applications('spark')

    def teardown_spark_app(self):
        pass

    @with_setup(set_spark_app, teardown_spark_app)
    def test_spark_applications(self):
        for app_type, apps in self._spark_apps.iteritems():
            if app_type.lower() == 'batch':
                for app in apps:
                    self.run_spark_batch_processing_app(app)

            elif app_type.lower() == 'streaming':
                for app in apps:
                    self.run_spark_stream_processing_app(app)

    def run_spark_batch_processing_app(self, app_details):
        pass

    def run_spark_stream_processing_app(self, app_details):
        pass






