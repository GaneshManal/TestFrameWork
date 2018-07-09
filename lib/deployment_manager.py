import requests
import time
import json
from util.common import get_logger


class DeploymentManager:
    dm_host, dm_port = None, None
    logger = get_logger('DeploymentManager')

    def __init__(self, dm_host, dm_port):
        self.dm_host = dm_host
        self.dm_port = dm_port

    def deploy_package(self, package_name):
        # url = 'http://%s:%s/api/dm/packages/%s?user.name=pnda' % (self.dm_host, self.dm_port, package_name)
        url = 'http://%s/api/dm/packages/%s?user.name=pnda' % (self.dm_host, package_name)
        self.logger.debug('inside deploy_package ,url is %s', url)
        resp = requests.put(url)
        self.logger.debug('resp status code is %s', resp.status_code)
        if resp.status_code == 200:
            return True
        return False

    @classmethod
    def _check_package_status(cls, pkg_name, exp_status):
        url = "http://%s:%s/packages/%s" % (cls.dm_host, cls.dm_port, pkg_name)
        cls.logger.debug('inside check package ,url is %s', url)
        while True:
            resp = requests.get(url)
            if json.loads(resp.text)["status"] == exp_status:
                break
            time.sleep(1)
        cls.logger.debug("ganesh --- its true")
        return True

    @classmethod
    def create_application(cls, pkg_name, app_name):
        cls.logger.debug('Package name - %s', pkg_name)
        cls.logger.debug('Application name - %s', app_name)
        cls._check_package_status(pkg_name, "DEPLOYED")


        payload_pkg_name = '_'.join(''.join(pkg_name.split('.')[:-2]).split('-')[:-1])
        payload = "APPLICATION_PAYLOAD.%s" % payload_pkg_name
        headers = {"content-type": "application/json"}
        uri = "http://%s:%d/applications/%s?user.name=pnda" % (cls.dm_host, cls.dm_port, app_name)

        res = requests.put(uri, data=json.dumps(payload), headers=headers)
        if res.status_code == 202:
            return True
        return False

    @classmethod
    def start_application(cls, app_name):
        cls._check_package_status(app_name, "CREATED")
        uri = "http://%s:%d/applications/%s/start?user.name=pnda" % (cls.dm_host, cls.dm_port, app_name)

        res = requests.post(uri)
        if res.status_code == 202:
            return True
        return False
