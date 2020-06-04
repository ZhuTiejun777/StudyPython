# 测试套件使用
import unittest
import time
from tool.HTMLTestRunner import HTMLTestRunner
# 创建套件对象
from case.TestTPShop import TestTPshop

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTPshop))

myReport = "./report/" + time.strftime("%Y_%m_%d %H%M%S") + "report.html"

with open(myReport,"wb") as f:
    runner = HTMLTestRunner(f,title="接口自动化测试",description="项目版本:1.0")
    runner.run(suite)