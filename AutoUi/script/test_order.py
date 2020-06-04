import logging
import time
import unittest
import utils

from page.cart_page import CartProxy
from page.index_page import IndexProxy
from page.my_order_page import MyOrderProxy
from page.order_page import OrderProxy
from page.order_pay_page import OrderPayProxy
from parameterized import parameterized

# 读取数据构造数据返回
# 参数化,数据驱动
def build_order():
    test_data = []
    json_data = utils.load_test_data("order.json")
    case_data = json_data.get("test01_order")
    test_data.append(case_data.get("exprct"))
    logging.info("test_data:{}".format(test_data))
    return test_data


def build_pay_order():
    test_data = []
    json_data = utils.load_test_data("order.json")
    case_data = json_data.get("test02_order")
    test_data.append(case_data.get("exprct"))
    logging.info("test_data:{}".format(test_data))
    return test_data


class TestOrder(unittest.TestCase):
    # fixture
    @classmethod
    def setUpClass(cls):
        # 获取浏览器驱动对象
        cls.driver = utils.DriverUtil.get_driver()
        # 获取用例页面
        cls.index_proxy = IndexProxy()
        cls.cart_proxy = CartProxy()
        cls.order_proxy = OrderProxy()
        cls.my_order_proxy = MyOrderProxy()
        cls.order_pay_proxy = OrderPayProxy()

    def setUp(self):
        # 打开首页
        self.driver.get("http://localhost")

    def tearDown(self):
        # 用例执行完毕后等待两秒
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        utils.DriverUtil.quit_driver()

    @parameterized.expand(build_order)
    def test01_order(self,expect):
        """下订单"""
        self.index_proxy.to_cart_page()
        self.cart_proxy.check_all_pay()
        time.sleep(5)
        self.order_proxy.submit_order()
        time.sleep(5)
        is_exist = utils.exist_text(expect)
        logging.info(is_exist)
        utils.screenshot()
        self.assertTrue(is_exist)

    @parameterized.expand(build_pay_order)
    def test02_order_pay(self,expect):
        """订单支付"""
        self.index_proxy.to_my_order()
        utils.switch_to_window()
        self.my_order_proxy.to_order_pay_page()
        utils.switch_to_window()
        self.order_pay_proxy.pay_complete()
        time.sleep(5)
        is_exist = utils.exist_text(expect)
        logging.info(is_exist)
        utils.screenshot()
        self.assertTrue(is_exist)