import paramiko


class RemoteServer(object):
    """
    Class to connect to a remote server
    """

    def __init__(self, node_ip, pem_file_location):
        self._node_ip = node_ip
        self._pem_file_location = pem_file_location

    @staticmethod
    def scp_to_node(client, src, dest):
        """
        Copies one file from local to remote destination
        :param client: client object
        :param src: source file location
        :param dest: destination location
        :return: None
        """
        ftp_client = client.open_sftp()
        ftp_client.put(src, dest)
        ftp_client.close()

    @staticmethod
    def exec_commands(client, cmd):
        """
        Executes a list of commands on the remote server
        :param client: client object
        :param cmd: list of commands
        :return: None
        """
        for command in cmd:
            print "Executing {}".format(command)
            stdin, stdout, stderr = client.exec_command(command)
            print stdout.read()

    @staticmethod
    def parse_node_details(node_details):
        """
        Parse the node details
        :param node_details: output of the consul commands
        :return: dict of node_details, dns as key and ip address as value
        """
        node_list = node_details.split("\n")[1:-1]
        node_dict = {}
        for node_str in node_list:
            node = node_str.split()
            node_dns = node[0]
            node_ip = node[1]
            node_dict[node_dns] = node_ip
        return node_dict

    def get_all_nodes(self, client):
        """
        gets the ip address and dns of all the nodes
        :param client: client object
        :return: dict of node_details, dns as key and ip address as value
        """
        stdin, stdout, stderr = client.exec_command(
            "consul members --http-addr http://$(hostname --ip-address):8500")
        node_dict = self.parse_node_details(stdout.read())
        return node_dict

    def connect(self):
        """
        connects to a remote server
        :return: connected client object
        """
        key = paramiko.RSAKey.from_private_key_file(self._pem_file_location)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self._node_ip, username="ec2-user", pkey=key)
        print "connection successfull"
        return client

    @staticmethod
    def close_connection(client):
        """
        closes the connection to the remote server
        :param client: client object
        :return: None
        """
        client.close()
        print "connection closed successfully"
