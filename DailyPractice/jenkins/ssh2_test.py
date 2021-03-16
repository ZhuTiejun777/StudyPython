import os
import paramiko
# 服务器信息
host1 = {"host": "192.168.3.138", "port": 22, "username": "root", "password": "zjport"}

#秘钥路径格式固定,需要paramiko.RSAKey.from_private_key_file()保存
#private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')

# paramiko中两种连接方式，传输（transport）,通道（channel）
# 传输（transport）:
# 先构建通道
# transport = paramiko.Transport((self.host, self.port))
# transport.connect(username=self.username, pkey=self.private_key)
# 在实例化
# ssh = paramiko.SSHClient();
# ssh._transport = self.__transport

# 通道（channel）:
# 实例化SSHClient
# client = paramiko.SSHClient()
# 连接SSH服务端,直接传入参数
# client.connect(hostname='192.168.163.129',port=22,username='root',pkey=private)
class SSHConnection(object):

    #初始化参数
    #秘钥连接不需要密码
    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']
        self.__k = None
        #秘钥路径
        #self.private_key = private_key

    #paramiko.Transport()方法中传入元组
    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    #可以加入ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   作用:不用验证
    def run_cmd(self, command):
        """执行shell命令,返回字典
        :param command:
        :return: """
        print(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = err if err else "正常执行"
        print(result)

    # # sftp = paramiko.SFTPClient.from_transport(transport) 获取到transport类,创建连接
    # # 本地路径,目标路径
    # def upload(self, local_path, target_path):
    #     # 连接，上传
    #     sftp = paramiko.SFTPClient.from_transport(self.__transport)
    #     # 将location.py 上传至服务器 /tmp/test.py
    #     sftp.put(local_path, target_path)
    #     print(os.stat(local_path).st_mode)
    #     # 增加权限
    #     sftp.chmod(target_path, os.stat(local_path).st_mode)
    #     sftp.chmod(target_path, 0o755)
    #     # 注意这里的权限是八进制的，八进制需要使用0o作 为前缀
    #
    # #sftp = paramiko.SFTPClient.from_transport(transport) 获取到transport类,创建连接
    # # 目标路径,本地路径
    # def download(self, target_path, local_path):
    #     # 连接，下载
    #     sftp = paramiko.SFTPClient.from_transport(self.__transport)
    #     # 将location.py 下载至服务器 /tmp/test.py
    #     sftp.get(target_path, local_path)

    # 销毁
    def __del__(self):
        self.close()



ssh = SSHConnection(host1)
ssh.connect()
ssh.run_cmd("mkdir 111")




