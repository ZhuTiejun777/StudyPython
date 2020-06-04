import time
import unittest

from config import BASE_DIR
from script.test_cart import TestCart
from script.test_login import TestLogin
from script.test_order import TestOrder
from utils import DriverUtil
from HTMLTestRunner import HTMLTestRunner


# 测试套件
suite = unittest.TestSuite()
DriverUtil.set_auto_quit(False)
# 添加用例
suite.addTest(unittest.makeSuite(TestLogin))
suite.addTest(unittest.makeSuite(TestCart))
suite.addTest(unittest.makeSuite(TestOrder))
# 关闭 退出驱动开关

# 运行
# unittest.TextTestRunner().run(suite)

report_path = BASE_DIR + "/report/reprot{}.html".format(time.strftime("%Y%m%d%H%M%S"))
with open(report_path, "wb") as f:
    runner = HTMLTestRunner(stream=f, title="tpshop商城", description="测试详情")
    runner.run(suite)
# 打开 退出驱动开关

DriverUtil.set_auto_quit(True)
# 退出驱动
DriverUtil.quit_driver()
