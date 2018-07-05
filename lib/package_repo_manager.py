import requests
import wget


class PackageRepoManager:
    prm_host, prm_port = None, None

    def __init__(self, prm_host, prm_port):
        self.prm_host, self.prm_port = prm_host, prm_port
        self._pkg_name = None

    def set_package_name(self, pkg_name):
        self._pkg_name = pkg_name

    @staticmethod
    def download_network_package(pkg_url):
        ret = wget.download(pkg_url)
        return ret

    def upload_package_to_repository(self, package_file):
        ret = requests.put("%s:%d/packages/%s.tar.gz?user.name=pnda" % (self.prm_host, self.prm_port, package_file),
                           data={'--upload-file': package_file})
        return ret
