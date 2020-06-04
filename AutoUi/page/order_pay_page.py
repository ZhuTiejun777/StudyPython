# 对象库层
from selenium.webdriver.common.by import By

from base.base_page import BasePage, BaseHandle


class OrderPayPage(BasePage):
    # init方法
    def __init__(self):
        # 调用父类init方法,实例化浏览器驱动对象
        super().__init__()
        self.pay_on_delivery = (By.CSS_SELECTOR, "img[src='/plugins/payment/cod/logo.jpg']")  # 货到付款
        self.verify_pay = (By.CSS_SELECTOR, ".button-style-5")  # 确认支付
        # self.pay_succeed = (By.CSS_SELECTOR, ".erhuh h3")  # 支付成功
        # 业务元素定位信息
        # 单选按钮--货到付款

        # 超链接--确认支付方式

    def find_pay_on_delivery(self):
        return self.find_element(self.pay_on_delivery)

    # 定位货到付款单选按钮

    def find_verify_pay(self):
        return self.find_element(self.verify_pay)
    # 定位确认支付方式超链接
    # def find_pay_succeed(self):
    #     return self.find_element(self.pay_succeed)


# 操作层
class OrderPayHandle(BaseHandle):
    # init方法
    def __init__(self):
        # 获取对象库层对象
        self.orderpay_page = OrderPayPage()

    # 点击货到付款
    def click_pay_on_delivery(self):
        self.orderpay_page.find_pay_on_delivery().click()

    def click_verify_pay(self):
        self.orderpay_page.find_verify_pay().click()

    # def text_pay_succeed(self):
    #     return self.orderpay_page.find_pay_succeed().text

    # 点击确认支付方式


# 业务层
class OrderPayProxy:
    # init方法
    def __init__(self):
        # 获取操作层对象
        self.orderpay_handle = OrderPayHandle()

    # 确认支付方式
    def pay_complete(self):
        """支付完成"""
        self.orderpay_handle.click_pay_on_delivery()
        self.orderpay_handle.click_verify_pay()

    # def order_pay_succeed(self):
    #     """获取支付成功提示信息"""
    #     return self.orderpay_handle.text_pay_succeed()
