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
            print( "Errors")
            print stderr.read()



    def copy_file(self, src, target, filename):
        pass

    def connect(self):
        k = paramiko.RSAKey.from_private_key_file(self._pem_file_location)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "connecting"
        c.connect(hostname = self._node_ip, username = "ec2-user", pkey = k)
        self.exec_commands(c, ["consul members --http-addr http://$(hostname --ip-address):8500"])
        print "connected"

    def parse_output(self):
        pass


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