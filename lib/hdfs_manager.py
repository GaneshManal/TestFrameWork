from pywebhdfs.webhdfs import PyWebHdfsClient


class HDFSManager(object):

    def __init__(self, host, port, user='hdfs'):
        self._hdfs = PyWebHdfsClient(host=host, port=port, user_name=user, timeout=None)

    def check_file_exists(self, path):
        try:
            self._hdfs.get_file_dir_status(path)
            return True
        except Exception:
            return False
