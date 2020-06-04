# 对象库层
from selenium.webdriver.common.by import By

from base.base_page import BasePage, BaseHandle


class OrderPage(BasePage):
    # init方法
    def __init__(self):
        # 调用父类init方法,实例化浏览器驱动对象
        super().__init__()

        # 业务元素定位信息
        # 超链接--提交订单

        self.recipients = (By.CSS_SELECTOR, "input[name='address_id']")  # 收件人
        self.submit_order = (By.CSS_SELECTOR, ".Sub-orders")  # 提交订单
        # self.order_succeed = (By.CSS_SELECTOR, ".erhuh h3")  # 提交成功

    # 定位提交订单超链接
    def find_recipients(self):
        return self.find_element(self.recipients)

    def find_submit_order(self):
        return self.find_element(self.submit_order)

    # def find_order_succeed(self):
    #     return self.find_element(self.order_succeed)


# 操作层
class OrderHandle(BaseHandle):
    # init方法
    def __init__(self):
        # 获取对象库层对象
        self.order_page = OrderPage()

    # 点击提交订单超链接
    def click_recipients(self):
        self.order_page.find_recipients().click()

    def click_submit_order(self):
        self.order_page.find_submit_order().click()

    # def text_order_succeed(self):
    #     return self.order_page.find_order_succeed().text


# 业务层
class OrderProxy:
    # init方法
    def __init__(self):
        # 获取操作层对象
        self.order_handle = OrderHandle()

    # 提交订单
    def submit_order(self):
        self.order_handle.click_recipients()
        self.order_handle.click_submit_order()

    # def order_succeed(self):
    #     """获取提交成功信息"""
    #     return self.order_handle.text_order_succeed()
