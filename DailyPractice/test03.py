import json
import re
import unittest
import random

import jsonpath
import paramiko
import requests


class test03(unittest.TestCase):

    def test01(self):
        sqlDict = {'table': 'auto_case_tmp',
                   'id': 3,
                   'number': 1,
                   'inputData': 'test',
                   'comment': '1234',
                   'needRun': '2',
                   'checkReWrite': '4',
                   'cStatus': '200'}
        insertStr = "insert into {} ({}) value ({})"
        columnStr = ""
        valueStr = ""
        number = 0
        for dictStr in sqlDict:
            number += 1
            if dict == "table":
                continue
            if number == len(sqlDict):
                columnStr = columnStr + dictStr
                valueStr = valueStr + str(sqlDict[dictStr])
            else:
                columnStr = columnStr + dictStr + ","
                valueStr = valueStr + str(sqlDict[dictStr]) + ","
        print(columnStr)
        print(valueStr)
        print(insertStr.format(sqlDict.get("table"), columnStr, valueStr))

    def test05(self):
        table = "test"
        item = {'table' : 'auto_case_tmp',
               'id' : 4,
               'number' : 1,
               'inputData' : 'test',
               'comment' : '1234',
               'needRun' : '2',
               'checkReWrite' : '4',
               'cStatus' : '200'}
        str = "insert into %s(%s) values(%s)" % (
            table,
            ",".join("{}".format(k) for k in item.keys()),
            ','.join("'{}'".format(k) for k in item.values())
        )
        print(str)

    def test06(self, length:int=10):
        #print(random.randint(0, 9))
        intStr = ""
        if length > 32:
            print("字符长度不可大于32!")
            length = 32
        number = length
        while length:
            if length == number:
                intStr += str(random.randint(1, 9))
            else:
                intStr += str(random.randint(0, 9))
            length -= 1
        return intStr

    def test07(self):
        print(self.test06(60))


    def test08(self):
        val = random.randint(0x4e00, 0x9fbf)
        print(chr(val))
        str = "test"

    def test09(self):
        strShell = "wc -l /home/store/224493763144187904/224493723487043584/221658682067255296/library/class_info"
        getPid = "ps -ef|grep tomcat|grep -v grep|awk '{print $2}'"
        getDirs = "cd /home/store/224493763144187904/224493723487043584/221658682067255296/library/; ls -l| grep '^-'| wc -l"
        getDirsName = "cd /home/store/224493763144187904/224493723487043584/221658682067255296/library/; ls -l |grep -v total|awk '{print $9}'"
        host = {"host": "192.168.66.179", "port": 22, "username": "root", "password": "Yrjk%test123"}
        mycon = SSHConnection(host)
        mycon.connect()
        res, err = mycon.run_cmd(getDirsName)
        print(res)
        dirsName = []
        for dirName in res:
            dirsName.append(dirName.split("\n")[0])
        print(dirsName)
        mycon.close()
        result = res[0].split(" ")[0]
        print(result)

    def test10(self):
        projectId = "1"
        storeId = "2"
        recordId = "3"
        dbName = "4"
        tableName = "5"
        strShell = "wc -l /home/store/" + projectId + "/" + storeId + "/" + recordId + "/" + dbName + "/" + tableName
        print(strShell)

    def test11(self):
        list1 = ["sss", 1]
        list2 = [1, "sss"]
        if list1 in list2:
            print("xiangtong")
        else:
            print("buxiangtong")
        #a = [x for x in list1 if x in list2]
        b = [y for y in (list1 + list2) if y not in [x for x in list1 if x in list2]]
        #print(a)
        if b == []:
            print("sss")

    def test12(self):
        reStr = "\d+"
        str = "sssssjsjnjnsjnsnjs11818fasdasda"
        pattern = re.compile(reStr)
        result = pattern.findall(str)
        print(result)


    def test13(self):
        url = "http://192.168.66.179:8080/DataFactory/queryAnalyserSummaryInfos"
        jsons = {"page":{"current":1,"size":10},"condition":{"projectId":"223826490662322176"}}
        response = requests.post(url=url, json=jsons)
        dictResponse = json.loads(response.text)
        #print(len(dictResponse.get("data")))
        print(jsonpath.jsonpath(dictResponse, "$.data"))
        print(len(jsonpath.jsonpath(dictResponse, "$.data")[0]))
        strList = "[{'id': '225996227458629632', 'analyseName': '自动化测试', 'comment': '自动化测试分析说明', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226000301281247232', 'analyseName': 'qajgqixerqmssafxtq', 'comment': '俒莩骾楟鶎鉎獹寜疄勠', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226004390534709248', 'analyseName': 'rwaiplqrnwikvxxlgc', 'comment': '淘酨鉄彽摱桇霖緆嵼筟', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226004914726240256', 'analyseName': 'utomlrvqdchafswlew', 'comment': '臯褱记旿楋戄饁拂筏纻', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226012107840159744', 'analyseName': 'pmcvhzlcxhdwwomntc', 'comment': '臡倛昶蹦熜義蠸咮縚泍', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226012233669279744', 'analyseName': 'ilhbkbngcrmhdmkcwy', 'comment': '懣罌関溟龏冧獸厧龃邽', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226013093526765568', 'analyseName': 'cbxchzmqbaupgwzizx', 'comment': '縿裘纂郖耙孛癣鯱泩者', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226018650966982656', 'analyseName': 'lwzbkdyswtvyxkscba', 'comment': '燞稧屓菫緲鹘憘舛始訕', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226019447956045824', 'analyseName': 'qujttdbqzywxktjvxymkbcgyuiwe', 'comment': '鬚疖姤趓偸部蝭孔瞾慳蛅軮糆靶菁尷零鵱懂倊', 'analyseStatus': '02', 'analyseMessage': '分析通过'}, {'id': '226019846419120128', 'analyseName': 'zjihtnskcvwrqjrhkvsmfnwluqjj', 'comment': '顰族禥脘鋼瘜白辜皞鰟槔釗瀂揨虋惰諓擸氓矅', 'analyseStatus': '02', 'analyseMessage': '分析通过'}]"
        print(len(list(strList)))

    @staticmethod
    def test17():
        list1 = ["sss","ttt"]
        list2 = ["kkk", "111"]
        return list1, list2

    def test14(self):
        list5, list6 = test03.test17()
        list = []
        list.extend(list5)
        print(list)

    def test15(self):
        print(
            random.randint(1000000000, 2147483647)
        )

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
        #print(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        res, err = stdout.readlines(), stderr.readlines()
        result = err if err else "正常执行"
        print(result)
        return res, err

    def __del__(self):
        self.close()
