# -*-coding:utf-8-*-
#-*-by zhutj 20200616-*-
import json
import os
import re
from datetime import datetime, timedelta

import requests


class getdatewrite():

    def __init__(self, dict):
        self.dict = dict

    def writefields(self, str):
        return str + ":" + self.dict[str] + "\n"

    def writedisposefields(self, str):
        return str + ":" + re.findall(">.*<", self.dict[str])[0][1:-1] + "\n"

    def continuewrite(self, f, *args):
        for str in args:
            if self.dict[str][0] == "<":
                f.write(self.writedisposefields(str))
            else:
                f.write(self.writefields(str))


def backupsfile(*args):
    str_now = datetime.now().strftime('%Y%m%d%H%M%S')
    for file in args:
        path = ".//" + file + ".txt"
        if (os.path.exists(path)):
            os.rename(path, ".//" + file + str_now + ".txt")


def getagodate(number, datestr):
    nowdate = datetime.now()
    agodate = nowdate + timedelta(days=-number)
    agodatestr = agodate.strftime('%Y-%m-%d')
    return agodatestr < datestr


def adddict(dict, *args):
    dicts = {}
    for str in args:
        if dict[str][0] == "<":
            dicts[str] = re.findall(">.*<", dict[str])[0][1:-1]
        else:
            dicts[str] = dict[str]
    return dicts


def getjson(url, headers, data):
    response = requests.post(url=url, headers=headers, data=data)
    return json.loads(response.text)


def statisticdata(list):
    list_statistic = []
    list_name = []
    for dict in list:
        list_name.append(dict["当前处理人"])
    for name in set(list_name):
        dict_statistic = {}
        count = 0
        list_number = []
        for dict in list:
            if name == dict["当前处理人"]:
                count += 1
                list_number.append(dict["编号"])
                dict_statistic["name"] = dict["当前处理人"]
                dict_statistic["count"] = count
                dict_statistic["编号"] = list_number
        list_statistic.append(dict_statistic)
    return list_statistic


def writedata(file, list):
    with open(".//" + file + ".txt", "a+") as f:
        f.write(datetime.now().strftime('%Y%m%d%H%M%S') + "\n")
        for dict in list:
            f.write(str(dict) + "\n")
    f.close()