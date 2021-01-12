# coding:utf-8
# by zhutj 20200518
# from kwl-banking-ccb
# python ${WORKSPACE}/TestConfig/SSHkwl-member.py
import paramiko

host = {"host": "192.168.3.38", "port": 22, "username": "root", "password": "zjport"}

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

mycon.run_cmd("nohup ps -ef | grep /usr/local/tomcat/tomcat6_8888-pen-manage | grep -v grep | awk '{print $2}' | xargs kill -9 >/usr/local/tomcat/tomcat6_8888-pen-manage/logs/SSHUpdate_kill.log 2>&1\n")

mycon.run_cmd(
    "nohup rm -r /usr/local/tomcat/tomcat6_8888-pen-manage/webapps/pen-manage/* >/usr/local/tomcat/tomcat6_8888-pen-manage/logs/SSHUpdate_rm.log 2>&1\n")

mycon.run_cmd(
    "wget http://192.168.3.239:8081/view/%E6%9C%B1%E9%93%81%E5%90%9B/job/PEN-V1.0_MANAGE\(%E7%9C%81%E5%8D%95%E4%B8%80%E7%AA%97%E5%8F%A3%E5%90%8E%E5%8F%B0-%E6%9C%B1%E9%93%81%E5%90%9B\)/ws/pen-manage-webapp/target/pen-manage.war -O /usr/local/tomcat/tomcat6_8888-pen-manage/webapps/pen-manage.war >/usr/local/tomcat/tomcat6_8888-pen-manage/logs/SSHUpdate_ftp.log 2>&1\n")

mycon.run_cmd("nohup unzip -o /usr/local/tomcat/tomcat6_8888-pen-manage/webapps/pen-portal.war -d /usr/local/tomcat/tomcat6_8888-pen-manage/webapps/pen-portal/ >/usr/local/tomcat/tomcat6_8888-pen-manage/logs/SSHUpdate_unzip.log 2>&1\n")

mycon.run_cmd("nohup /usr/local/tomcat/tomcat6_8888-pen-manage/bin/startup.sh >/usr/local/tomcat/tomcat6_8888-pen-manage/logs/SSHUpdate_starup.log 2>&1\n")

mycon.close()




