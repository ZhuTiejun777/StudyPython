# 参数化,数据驱动
# 创建测试类
import logging
import time
import unittest

import utils
from page.goods_detail_page import GoodsDetailProxy
from page.goods_search_page import GoodsSearchProxy
from page.index_page import IndexProxy
from utils import DriverUtil
from parameterized import parameterized


# 读取数据构造数据返回
def build_data():
    test_data = []
    json_data = utils.load_test_data("cart.json")
    for i in json_data.values():
        for case_data in i:
            test_data.append((case_data.get("goods_name"),
                              case_data.get("expect")))
    logging.info("test_data:{}".format(test_data))
    return test_data


class TestCart(unittest.TestCase):

    # fixture
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverUtil.get_driver()
        cls.index_proxy = IndexProxy()
        cls.goods_search_proxy = GoodsSearchProxy()
        cls.goods_detail_proxy = GoodsDetailProxy()

    def setUp(self):
        # 打开首页
        self.driver.get("http://localhost")

    def tearDown(self):
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        DriverUtil.quit_driver()

    # 创建测试方法,断言
    # 参数化-数据驱动
    @parameterized.expand(build_data)
    def test_cart(self, goods_name, expect):
        """加入购物车"""
        logging.info("goods_name:{},expect:{}".format(goods_name, expect))
        self.index_proxy.search_goods(goods_name)
        self.goods_search_proxy.to_goods_detail_page(goods_name)
        self.goods_detail_proxy.join_goods_to_cart()
        time.sleep(2)
        # 注意点 -- 如果定位失败了怎么排查问题
        utils.screenshot()
        is_success = self.goods_detail_proxy.is_join_cart_success(expect)
        self.assertTrue(is_success)
# 参数化,数据驱动
