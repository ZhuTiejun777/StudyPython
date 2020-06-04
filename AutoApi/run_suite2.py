import unittest
import time
import app
from case.TestCollections import TestCollections
from case.TestLogin import TestLogin
from tools.HTMLTestRunner import HTMLTestRunner

# 创建套件 添加用例
suite = unittest.TestSuite()
suite.addTest(TestLogin("test03_login_success"))
suite.addTest(TestCollections("test02_cancel"))

# 创建运行器
unittest.TextTestRunner().run(suite)
# file = app.BASE_DIR + "/report/reprot{}.html".format(time.strftime("%Y%m%d%H%M%S"))
# with open(file, "wb") as f:
#     runner = HTMLTestRunner(f, title="测试报告", description="自动化测试")
#     # 执行用例
#     runner.run(suite)
