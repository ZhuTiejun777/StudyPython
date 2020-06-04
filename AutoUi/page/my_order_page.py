# 对象库层
from selenium.webdriver.common.by import By

from base.base_page import BasePage, BaseHandle


class MyOrderPage(BasePage):
    # init方法
    def __init__(self):
        # 调用父类init方法,实例化浏览器驱动对象
        super().__init__()

        # 页面元素定位信息
        # 超链接--待付款
        self.now_pay = (By.CSS_SELECTOR, ".ps_lj")  # 立即支付
        self.wait_pay = (By.XPATH, "//a[text()='待付款']")  # 待付款

        # 超链接--立即支付

    # 定位待付款超链接
    def find_now_pay(self):
        return self.find_element(self.now_pay)

    def find_wait_pay(self):
        return self.find_element(self.wait_pay)
    # 定位立即支付超链接


# 操作层
class MyOrderHandle(BaseHandle):
    # init方法
    def __init__(self):
        # 获取对象库层对象
        self.myorder_page = MyOrderPage()

    # 点击待付款
    def click_now_pay(self):
        self.myorder_page.find_now_pay().click()

    def click_wait_pay(self):
        self.myorder_page.find_wait_pay().click()

    # 点击立即支付


# 业务层
class MyOrderProxy:
    # init方法
    def __init__(self):
        # 获取操作层对象
        self.myorder_handle = MyOrderHandle()

    # 去支付
    def to_order_pay_page(self):
        """待付款 立即支付 进入选择付款方式界面"""
        self.myorder_handle.click_wait_pay()
        self.myorder_handle.click_now_pay()
