import paramiko
class RemoteServer(object):
    _node_ip = None
    _pem_file_location = None

    def __init__(self, node_ip, pem_file_location):
        self._node_ip = node_ip
        self._pem_file_location = pem_file_location

    def exec_commands(self, c, cmd):
        for command in cmd:
            print "Executing {}".format(command)
            stdin , stdout, stderr = c.exec_command(command)
            print stdout.read()
            print("Errors")
            print stderr.read()

    def parse_node_details(self, node_details):
        node_list = node_details.split("\n")
        node_list = node_list[1: len(node_list)-1]
        node_dict = {}
        for node_str in node_list:
            node = node_str.split()
            node_dns = node[0]
            node_ip = node[1]
            node_dict[node_dns] = node_ip
        return node_dict

    def get_all_nodes(self, client):
        stdin, stdout, stderr = client.exec_command("consul members --http-addr http://$(hostname --ip-address):8500")
        node_dict = self.parse_node_details(stdout.read())
        return node_dict

    def copy_file(self, src, target, filename):
        pass

    def connect(self):
        key = paramiko.RSAKey.from_private_key_file(self._pem_file_location)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print "connecting"
        client.connect(hostname = self._node_ip, username = "ec2-user", pkey = key)
        # self.exec_commands(client, ["consul members --http-addr http://$(hostname --ip-address):8500"])
        print "connection successfull"
        return client

    def parse_output(self):
        pass

    def close_connection(self, client):
        client.close()
        print "connection closed successfully"


# import paramiko
# k = paramiko.RSAKey.from_private_key_file("/Users/whatever/Downloads/mykey.pem")
# c = paramiko.SSHClient()
# c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# print "connecting"
# c.connect( hostname = "www.acme.com", username = "ubuntu", pkey = k )
# print "connected"
# commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
# for command in commands:
# 	print "Executing {}".format( command )
# 	stdin , stdout, stderr = c.exec_command(command)
# 	print stdout.read()
# 	print( "Errors")
# 	print stderr.read()
# c.close()