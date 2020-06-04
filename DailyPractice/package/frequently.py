import time
import os
import re
import json
import random
import urllib
from urllib import parse
import requests
import shutil
import sys
import paramiko
import pymysql
import unittest
import logging
from parameterized import parameterized

from package.HTMLTestRunner import HTMLTestRunner

path = os.path.dirname(os.path.abspath(__file__))
executepath = sys.argv[1]


class SSHCon(object):

    def __init__(self, dist):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=dist['host'],
                         port=dist['port'],
                         username=dist['username'],
                         password=dist['password'])

    def cmd(self, command):
        print(command)
        self.ssh.exec_command(command)
        time.sleep(1)

    def close(self):
        self.ssh.close()


class mysql(object):

    def __init__(self, db):
        self.connect = pymysql.connect(host=db['host'], port=db['port'],
                                       user=db['user'], password=db['password'],
                                       database=db['database'], charset=db['charset'])
        self.cursor = self.connect.cursor()

    def executesql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            self.cursor.fetchall()
        except:
            self.connect.rollback()

    def close(self):
        self.cursor.close()
        self.connect.close()


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        pass

    @parameterized.expand("date")
    def test_case(self):
        self.assertEqual("assert", "porxy")

    @unittest.skip("reason")
    def test_pass(self):
        pass


def runsuite():
    report_path = path + "/report/reprot{}.html".format(time.strftime("%Y%m%d%H%M%S"))
    suite = unittest.TestSuite()
    suite.addTests(map(TestCase, ["test_case", "test_pass"]))
    unittest.TextTestRunner().run(suite)
    with open(report_path, "wb") as f:
        runner = HTMLTestRunner(stream=f, title="测试报告", description="测试详情")
        runner.run(suite)


def copy(executepath, lists):
    for list in lists:
        shutil.copyfile(executepath + list[0], executepath + list[1])


def get_url(url, headers, json):
    response = requests.post(url=url, headers=headers, json=json)
    print(response.status_code)
    print(response.text)


def readjson(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        text = json.load(f)
    return text


def translationurl(url):
    return parse.unquote(url)
