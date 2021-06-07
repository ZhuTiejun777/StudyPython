import json
import time

from util.SSHUtil import SSHUtil

config_json = {
    "default_info": {
        "username": "loan",
        "password": "loan!1234",
        "port": 22
    },
    "server_info": [
        {
            "host": "192.168.66.110",
            "servername": "192.168.66.110"
        }, {
            "host": "192.168.66.112",
            "servername": "192.168.66.112"
        }, {
            "host": "192.168.66.109",
            "servername": "192.168.66.112"
        }, {
            "host": "192.168.66.113",
            "servername": "192.168.66.112"
        }
    ]
}


def sshjvm(interval, count, rootPath, sign):
    getJpsList = "jps |grep -v Jps|awk '{print $1}'"
    sshCommandList = readConfigJson()
    for sshCommand in sshCommandList:
        res, err = sshCommand.get_cmd(getJpsList)
        sshCommand.run_cmd("mkdir " + rootPath)
        for pid in res:
            sshCommand.run_cmd(getSSHGcutil(pid.split("\n")[0], interval, count, rootPath, sign))
            sshCommand.run_cmd(getSSHGC(pid.split("\n")[0], interval, count, rootPath, sign))

def readConfigJson():
    sshCommandList = []
    if config_json["default_info"]:
        ssh_dict = {
            "username": config_json["default_info"]["username"],
            "password": config_json["default_info"]["password"],
            "port": config_json["default_info"]["port"],
        }
        for sshJson in config_json["server_info"]:
            ssh_dict["host"] = sshJson["host"]
            ssh_util = SSHUtil(ssh_dict)
            ssh_util.connect()
            sshCommandList.append(ssh_util)
    return sshCommandList


def getSSHGcutil(pid, interval, count, rootPath, sign):
    path = rootPath + "/gcutil-" + pid + "-" + str(interval) + "-" + str(count) + "-" + time.strftime(
        "%Y%m%d") + "-" + sign + ".log"
    return "nohup jstat -gcutil {} {} {} >{} 2>&1 &".format(pid, interval, count, path)


def getSSHGC(pid, interval, count, rootPath, sign):
    path = rootPath + "/gc-" + pid + "-" + str(interval) + "-" + str(count) + "-" + time.strftime("%Y%m%d") + "-" + sign + ".log"
    return "nohup jstat -gc {} {} {} >{} 2>&1 &".format(pid, interval, count, path)


if __name__ == '__main__':
    interval = 1000 * 5
    count = 12 * 60 * 3
    path = "/app/logs/jvm/" + time.strftime("%Y%m%d%H%M%S")
    sgin = "3"

    # print(getSSHGcutil(pid, interval, count, path, "ss"))
    # print(getSSHGC(pid, interval, count, path, "ss"))

    sshjvm(interval, count, path, sgin)
    print(path)
    # /app/logs/jvm/20210528133218
