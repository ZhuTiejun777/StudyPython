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
        }
    ]
}

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



if __name__ == '__main__':
    ssh_pid_cpu_start = "top -b -n 1 -H -p "
    ssh_pid_cpu_end = "|sed -n '8,20p'|awk '{print $1,$9}'"
    ssh_jps = "jps |grep -v Jps|awk '{print $1}'"
    ssh_jstack = "jstack -l {} -J-d64|grep '{}' -A 7"
    ssh_dict = {
        "host": "192.168.66.110",
        "username": "loan",
        "password": "loan!1234",
        "port": 22
    }
    print(ssh_jstack.format("pid", "str_nid"))
    ssh_util = SSHUtil(ssh_dict)
    ssh_util.connect()
    pid = ssh_util.get_cmd(ssh_jps)[0][1].split("\n")[0]
    print(pid)
    list_tid = []
    for i in range(3):
        time.sleep(1)
        res = ssh_util.get_cmd(ssh_pid_cpu_start + pid + ssh_pid_cpu_end)[0]
        list_tid.append(res[0].split("\n")[0].split(" ")[0])
        print(res[0].split("\n")[0].split(" ")[0])
    if list_tid[0] == list_tid[1] == list_tid[2]:
        str_nid = "%#x" % int(list_tid[0])
        print(str_nid)
        jstack_result = ssh_util.get_cmd(ssh_jstack.format(pid, str_nid))
        print(jstack_result)

    ssh_util.close()

