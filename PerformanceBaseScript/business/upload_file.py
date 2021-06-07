import os

from util.SSHUtil import SSHUtil

config_json = {
    "default_info": {
        "username": "root",
        "password": "yrjk%!123098",
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


def get_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list = files
    return file_list

if __name__ == '__main__':
    dir_list = ["20330401", "20330501", "20330502", "20330503"]
    dir_date = "20330502/raise_limit_20330502"
    timeTime = "1622789567"
    root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('business')[0], "result/" + timeTime, dir_date)
    upoad_path = "/app/loan/sftpfile/loanV3.0/MEITUAN20210531/balance/" + dir_date
    file_list = get_file_list(root_path)

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
            ssh_util.run_cmd("rm -rf " + upoad_path)
            ssh_util.run_cmd("mkdir " + upoad_path)
            for file_path in file_list:
                ssh_util.upload(root_path + "/" + file_path, upoad_path + "/" + file_path)
            ssh_util.close()
