from selenium.webdriver.common.by import By

# 个人中心页
from base.base_page import BasePage


class HomePage(BasePage):
    """对象库层"""

    def __init__(self):
        super().__init__()
        # self.my_order = (By.XPATH, "//a[text()='我的订单']")  # 我的订单
        # self.index = (By.XPATH, "//a[text()='首页']")  # 首页
        self.username = (By.CSS_SELECTOR, ".mu-m-phone")  # 用户名

    # def find_my_order(self):
    #     return self.page_base(self.my_order)

    # def find_index(self):
    # return self.page_base(self.index)

    def find_username(self):
        return self.find_element(self.username)


class HomeHandle():
    """操作层"""

    def __init__(self):
        self.home_page = HomePage()

    # def click_my_order(self):
    #     self.home_page.find_my_order().click()

    # def click_index(self):
    # self.home_page.find_index().click()

    def text_username(self):
        return self.home_page.find_username().text


class HomeProxy():
    """业务层"""

    def __init__(self):
        self.home_handle = HomeHandle()

    def login_succeed_username(self):
        """登录成功用户信息"""
        return self.home_handle.text_username()

    # def to_my_order_page(self):
    #     """进入我的订单"""
    #     self.home_handle.click_my_order()

    # def go_index_page(self):
    #     """进入首页"""
    #     self.home_handle.click_index()
