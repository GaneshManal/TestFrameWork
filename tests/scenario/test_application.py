import sys
import json
from nose.tools import with_setup
from util.pnda import ClusterConnection
from lib.kafka_manager import KafkaManager
from lib.deployment_manager import DeploymentManager
from lib.package_repo_manager import PackageRepoManager
from lib.hdfs_manager import HDFSManager
from util.common import get_logger


class TestApplication(object):
    _deployment_manager, _package_repo_manager = None, None
    _kafka_manager, _hdfs_manager = None, None
    logger = get_logger('TestApplication')

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

    # @with_setup(set_spark_app, teardown_spark_app)
    def test_spark_applications(self):
        self._spark_apps = self._conn_obj.get_input_applications('spark')
        for app_type, apps in self._spark_apps.iteritems():
            if app_type.lower() == 'batch':
                self.logger.info('Batch apps: %s', json.dumps(apps))
                for x_app in apps:
                    self.run_spark_batch_processing_app(x_app)

            elif app_type.lower() == 'streaming':
                for x_app in apps:
                    self.run_spark_stream_processing_app(x_app)

    def run_spark_batch_processing_app(self, app_data):
        app_name = app_data.keys()[0]
        self.logger.info('Running Spark Batch processing app - %s' % app_name)

        app_details = app_data.get(app_name)

        # Create kafka Topic
        ret = self._kafka_manager.create_topic(app_details.get('topic-name', 'test-name'))
        if not ret:
            self.logger.error("Unable to Create Kafka topic.")
            sys.exit(1)
        self.logger.info('Success - Kafka topic created.')

        # Run producer to generate test data
        ret = self._kafka_manager.run_producer(app_details)
        if not ret:
            self.logger.error("Failed to produce data.")
            sys.exit(1)
        self.logger.info('Success - Data produced.')

        # Download application package
        self.logger.debug("Package Link - %s", app_details.get('package-location'))
        ret = self._package_repo_manager.download_network_package(app_details.get('package-location'))
        package_file = ret
        if not ret:
            self.logger.error("Unable to download the package.")
            sys.exit(1)
        self.logger.info('Success - Package Downloaded..')

        # Upload application package package repository
        ret = self._package_repo_manager.upload_package_to_repository(package_file)
        if not ret:
            self.logger.error("Failed to upload package to package repository")
            sys.exit(1)
        self.logger.info('Success - Package uploaded.')

        # Deploy the package
        ret = self._deployment_manager.deploy_package(app_details.get('package-name'))
        if not ret:
            self.logger.error("Deployment Manager Failed to deploy the package")
            sys.exit(1)
        self.logger.info('Success - Package deployed.')

        # Create application for the Package
        ret = self._deployment_manager.create_application(app_details.get('package-name'), app_details.get('name'))
        if not ret:
            self.logger.error("Deployment Manager Failed to create the application")
            sys.exit(1)
        self.logger.info('Success - Application created.')

        # Start application
        ret = self._deployment_manager.start_application(app_details.get('name'))
        if not ret:
            self.logger.error("Deployment Manager Failed to start the application")
            sys.exit(1)
        self.logger.info('Success - Application started')

    def run_spark_stream_processing_app(self, app_details):
        pass
