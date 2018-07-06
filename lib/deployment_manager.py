import requests
import time
import json


class DeploymentManager:
    dm_host, dm_port = None, None

    def __init__(self, dm_host, dm_port):
        self.dm_host = dm_host
        self.dm_port = dm_port

    def deploy_package(self, package_name):
        url = "http://%s:%d/packages/%s?user.name=pnda" % (self.dm_host, self.dm_port, package_name)
        res = requests.put(url)
        if res.status_code == 202:
            return True
        return False

    @classmethod
    def _check_package_status(cls, pkg_name, exp_status):
        url = "http://%s:%d/packages/%s" % (cls.dm_host, cls.dm_port, pkg_name)
        while True:
            resp = requests.get(url)
            if json.loads(resp.text)["status"] == exp_status:
                break
            time.sleep(1)
        return True

    @classmethod
    def create_application(cls, pkg_name, app_name):
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
