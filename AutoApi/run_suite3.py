import time
import unittest
import app

from case.TestLogin import TestLogin
from tools import HTMLTestRunner

# 创建套件 添加用例


# 创建运行器
# unittest.TextTestRunner().run(suite)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestLogin))
report_path = app.BASE_DIR + "/report/{}.html".format(time.strftime("%Y%m%d%H%M%S"))
with open(report_path,"wb") as f:
    runner = HTMLTestRunner(stream=f,title="测试报告",description="测试详情")
    runner.run(suite)



