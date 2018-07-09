import os
import requests
import wget
from util.common import get_logger
import time


class PackageRepoManager:
    prm_host, prm_port = None, None
    logger = get_logger('PackageRepoManager')

    def __init__(self, prm_host, prm_port):
        self.prm_host, self.prm_port = prm_host, prm_port
        self._pkg_name = None

    def set_package_name(self, pkg_name):
        self._pkg_name = pkg_name

    @staticmethod
    def download_network_package(pkg_url):
        # Overwrite file if already exists
        filename = pkg_url.split('/')[-1]
        file_path = os.getcwd() + os.path.sep + filename

        epoch_str = str(time.time())
        if os.path.exists(file_path):
            os.rename(file_path, file_path + epoch_str)
        filename = wget.download(pkg_url)
        return filename

    def upload_package_to_repository(self, package_file):
        self.logger.debug('Filename - %s', package_file)
        url = 'http://%s:%s/packages/%s?user.name=pnda' % (self.prm_host, self.prm_port, package_file)
        self.logger.debug('Request URL - %s', url)
        resp = requests.put(url, data={'--upload-file': package_file})
        self.logger.debug('response - %d', resp.status_code)
        self.logger.debug('response text - %s', resp.text)
        if resp.status_code == 200:
            return True
        return False
