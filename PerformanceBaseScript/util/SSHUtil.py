# -*- coding: UTF-8 -*-
__Author__ = "zhutiejun777"
__Date__ = "2020/05/15"

import paramiko
import logging
import os

from LogGer import LogGer

LogGer(str(os.path.basename(__file__))[:-3])


class SSHUtil(object):

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
        logging.info(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        res, err = stdout.read(), stderr.read()
        result = err if err else "正常执行"
        print(result)

    def get_cmd(self, command):
        logging.info(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        # res, err = stdout.read(), stderr.read()
        res, err = stdout.readlines(), stderr.readlines()
        # print(err)
        return res, err
        # result = err if err else "正常执行"
        # print(result)

    # 本地路径,目标路径
    def upload(self, local_path, target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)
        # print(os.stat(local_path).st_mode)
        sftp.chmod(target_path, os.stat(local_path).st_mode)
        sftp.chmod(target_path, 0o755)
        logging.info("{} 文件上传成功: {}".format(local_path, target_path))

    # 目标路径,本地路径
    def download(self, target_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(target_path, local_path)

    def __del__(self):
        self.close()
