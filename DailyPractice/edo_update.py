# coding:utf-8
# by zhutj 20210312
import paramiko

host = {"host": "192.168.3.25", "port": 22, "username": "root", "password": "zjport"}


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

mycon.run_cmd("nohup ps -ef | grep /usr/local/tomcat/tomcat8_jdk1.8_9900 | grep -v grep | awk '{print $2}' | xargs kill -9")

mycon.run_cmd("nohup rm -rf /usr/local/tomcat/tomcat8_jdk1.8_9001_EDO/webapps/szpen-edo-web /usr/local/tomcat/tomcat8_jdk1.8_9001_EDO/webapps/szpen-edo-web.war")

mycon.run_cmd("wget http://192.168.3.239:8081/view/%E6%9C%B1%E9%93%81%E5%90%9B/job/PEN-V1.0_szpen-edo-webapp\(%E6%95%B0%E5%AD%97%E5%8D%95%E4%B8%80%E7%AA%97%E5%8F%A3%E5%8D%95%E8%AF%81%E7%94%B5%E5%AD%90%E5%8C%96-%E6%9C%B1%E9%93%81%E5%90%9B\)/ws/szpen-edo-webapp/target/szpen-edo-web.war -O /usr/local/tomcat/tomcat8_jdk1.8_9001_EDO/webapps/szpen-edo-web.war")

mycon.run_cmd("nohup /usr/local/tomcat/tomcat8_jdk1.8_9001_EDO/bin/startup.sh")

mycon.close()