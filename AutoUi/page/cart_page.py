from selenium.webdriver.common.by import By

from base.base_page import BasePage


# 购物车页
class CartPage(BasePage):
    """对象库层"""

    def __init__(self):
        super().__init__()
        self.check_all = (By.CSS_SELECTOR, ".pa-le-28 .checkCart")  # 全选
        self.go_pay = (By.XPATH, "//a[text()='去结算']")

    def find_check_all(self):
        return self.find_element(self.check_all)

    def find_go_pay(self):
        return self.find_element(self.go_pay)


class CartHandle():
    """操作层"""

    def __init__(self):
        self.cart_page = CartPage()

    def click_check_all(self):
        if not self.cart_page.find_check_all().is_selected():
            self.cart_page.find_check_all().click()

    def click_go_pay(self):
        self.cart_page.find_go_pay().click()


class CartProxy():
    """业务层"""

    def __init__(self):
        self.cart_handle = CartHandle()

    def check_all_pay(self):
        """全选商品 去结算"""
        self.cart_handle.click_check_all()
        self.cart_handle.click_go_pay()
