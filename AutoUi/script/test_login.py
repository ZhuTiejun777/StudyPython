import logging
import time
import unittest
import utils

from page.index_page import IndexProxy
from page.login_page import LoginProxy
from parameterized import parameterized


# 创建测试类

# 读取数据构造数据返回
def login_data():
    test_data = []
    json_data = utils.load_test_data("login.json")
    for case_data in json_data.values():
        test_data.append((case_data.get('username'),
                          case_data.get('password'),
                          case_data.get('verify_code'),
                          case_data.get('expect')))
    logging.info("test_data:{}".format(test_data))
    return test_data


# 测试类

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = utils.DriverUtil.get_driver()
        cls.index_proxy = IndexProxy()
        cls.login_proxy = LoginProxy()

    def setUp(self):
        self.driver.get("http://localhost")
        self.index_proxy.to_login_page()

    def tearDown(self):
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        utils.DriverUtil.quit_driver()

    # 参数化,数据驱动
    # 测试方法,断言
    @parameterized.expand(login_data)
    def test_login(self, username, password, verify_code, expect):
        """登录"""
        logging.info("username:{}password:{}verify_code:{}expect:{}".
                     format(username, password, verify_code, expect))
        self.login_proxy.login(username, password, verify_code)
        time.sleep(5)
        utils.screenshot()
        self.assertIn(expect, self.driver.title)


