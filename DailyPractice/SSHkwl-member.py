# coding:utf-8
# by zhutj 20200518
# from kwl-banking-ccb
# python ${WORKSPACE}/TestConfig/SSHkwl-member.py
import paramiko

host = {"host": "192.168.1.18", "port": 22, "username": "root", "password": "zjport"}


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

mycon.run_cmd("nohup ps -ef|grep member-8081|grep -v grep|awk '{print $2}'|xargs kill -9")

mycon.run_cmd(
    "rm -rf /usr/local/etc-member/member-8081/webapps/member.war /usr/local/etc-member/member-8081/webapps/member")

mycon.run_cmd(
    "wget http://192.168.3.239:8081/view/%E6%9C%B1%E9%93%81%E5%90%9B/job/KWL-V1.0_member\(ETC%E5%90%8E%E5%8F%B0%E4%BC%9A%E5%91%98%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F-%E6%9C%B1%E9%93%81%E5%90%9B\)/ws/kwl-multiproject/kwl-webapps-member/target/member.war -O /usr/local/etc-member/member-8081/webapps/member.war")

mycon.run_cmd("export JAVA_HOME=/usr/local/jdk/jdk1.8.0_121; nohup /usr/local/etc-member/member-8081/bin/startup.sh")

mycon.close()
