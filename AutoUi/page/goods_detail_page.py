import time
from selenium.webdriver.common.by import By

from base.base_page import BasePage, BaseHandle

# 对象库层
from utils import DriverUtil


class GoodsDetailPage(BasePage):
    # init方法
    def __init__(self):
        # 调用父类init方法,实例化浏览器驱动对象
        super().__init__()

        # 业务元素定位信息
        # 超链接-加入购物车
        self.join_cart = (By.ID, 'join_cart')
        # span-加入结果提示
        self.join_result = (By.CSS_SELECTOR, "div.conect-title>span")

    # 定位加入购物车超链接
    def find_join_cart(self):
        return self.find_element(self.join_cart)

    # 定位加入结果提示信息
    def find_join_result(self):
        return self.find_element(self.join_result)


# 操作层
class GoodsDetailHandle(BaseHandle):
    # init方法
    def __init__(self):
        # 获取对象库层对象
        self.goods_detail_page = GoodsDetailPage()

    # 点击加入购物车超链接
    def click_join_cart(self):
        self.goods_detail_page.find_join_cart().click()

    # 获取加入结果提示信息文本--返回文本信息
    def get_join_result(self):
        return self.goods_detail_page.find_join_result().text


# 业务层
class GoodsDetailProxy:
    # init方法
    def __init__(self):
        # 获取操作层对象
        self.driver = DriverUtil.get_driver()
        self.goods_detail_handle = GoodsDetailHandle()

    # 添加商品到购物车
    def join_goods_to_cart(self):
        self.goods_detail_handle.click_join_cart()

    # 判断是否加入成功 -- 返回是否成功布尔值
    def is_join_cart_success(self, expect):
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        result = self.goods_detail_handle.get_join_result()
        return expect == result
