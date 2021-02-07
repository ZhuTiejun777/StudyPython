# _*_coding:utf-8_*_


import paramiko


class SSHConnection(object):

    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.pwd = host_dict['pwd']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        """
         执行shell命令,返回字典
        :param command:
        :return:
        """
        print(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = err if err else "正常执行"
        print(result)

    # 结束
    def __del__(self):
        self.close()


# ---------------------------------------------------------------


def deployTheApp(path, url):
    host1 = {"host": "192.168.3.238", "port": 22, "username": "root", "pwd": "zjport"}
    ssh = SSHConnection(host1)
    ssh.connect()
    # ssh=SSHCon(linux_ip,linux_port,linux_username,linux_pwd)

    # ----------------------1、删除tsn-v2.0.zip包-------------------------
    ssh.run_cmd("rm -rf " + path + "tsn-v2.0.zip \n")
    # ----------------------2、拷贝Jenkins服务器上的包到目录下-------------------------
    ssh.run_cmd("wget --directory-prefix=" + path + " " + url + " \n")
    # ----------------------3、解压tsn-v2.0.zip包-------------------------
    ssh.run_cmd("unzip -o " + path + "tsn-v2.0.zip -d " + path + " \n")

    ssh.run_cmd("bash -lc 'cd /usr/share/nginx/html/TSN-DEV/tsn-v2.0/;nohup npm run build:;'")

    # 退出登录
    ssh.close()


if __name__ == "__main__":
    path = '/usr/share/nginx/html/TSN-DEV/'
    url = 'http://192.168.3.239:8081/view/%E8%B4%A7%E4%BB%A3%E8%BD%AF%E4%BB%B6/job/TSN-V1.0\(VUE%E9%9D%99%E6%80%81%E9%A1%B5%E9%9D%A2-%E8%B4%BE%E6%B5%B7%E6%98%8E\)/ws/tsn-v2.0/*zip*/tsn-v2.0.zip'
    deployTheApp(path, url)



