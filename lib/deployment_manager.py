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
        url = 'http://%s:%s/packages/%s?user.name=pnda' % (self.dm_host, self.dm_port, package_name)
        resp = requests.put(url)

        if resp.status_code == 202:
            return True
        elif resp.status_code == 409:
            return True
        return False

    def _check_package_status(self, component, pkg_name, exp_status):
        url = "http://%s:%s/%s/%s" % (self.dm_host, self.dm_port, component, pkg_name)
        while True:
            resp = requests.get(url)
            if json.loads(resp.text)["status"] == exp_status:
                break
            time.sleep(1)
        self.logger.debug("ganesh --- its true")
        return True

    def create_application(self, app_details):
        pkg_name = app_details.get('package-name')
        self.logger.debug('Package name - %s', pkg_name)
        self.logger.debug('Application name - %s', app_details.get('name'))
        self._check_package_status("packages", pkg_name,  "DEPLOYED")

        payload_pkg_name = '_'.join(''.join(pkg_name.split('.')[:-2]).split('-')[:-1])
        payload = app_details.get('payload')
        self.logger.debug('payload: %s', json.dumps(payload))
        self.logger.debug('payload pkg name- %s', payload_pkg_name)
        headers = {"content-type": "application/json"}
        uri = "http://%s:%s/applications/%s?user.name=pnda" % (self.dm_host, self.dm_port, app_details.get('name'))
        res = requests.put(uri, data=json.dumps(payload), headers=headers)
        if res.status_code == 202:
            return True
        elif res.status_code == 409:
            return True
        return False

    def start_application(self, app_details):
        app_name = app_details.get('name')
        self._check_package_status("applications", app_name, "CREATED")
        uri = "http://%s:%d/applications/%s/start?user.name=pnda" % (self.dm_host, self.dm_port, app_name)
        res = requests.post(uri)
        if res.status_code == 202:
            return True
        return False
