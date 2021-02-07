# coding:utf-8
# by zhutj 20200518
# from kwl-banking-ccb
# python ${WORKSPACE}/TestConfig/SSHkwl-member.py
import sys
import paramiko

host = {"host": "192.168.1.18", "port": 22, "username": "root", "password": "zjport"}

newVersion = sys.argv[1]
replaceCommand = "/etc/kubernetes/yaml/etc/applymember.sh {0}".format(newVersion)

class SSHConnection(object):

    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        print(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        res, err = stdout.read(), stderr.read()
        result = err if err else "正常执行"
        print(result)

    def __del__(self):
        self.close()


mycon = SSHConnection(host)
mycon.connect()

mycon.run_cmd(replaceCommand)

mycon.close()
