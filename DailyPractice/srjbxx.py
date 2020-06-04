import pymysql
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json


class jbxxlr(object):

    # 初始化浏览器驱动
    def __init__(self, url, cookie):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        self.driver.add_cookie(cookie_dict=cookie)
        self.driver.refresh()

    # 关闭浏览器驱动
    def quit_driver(self):
        self.driver.quit()

    # 进入新增界面
    def get_driver(self):
        self.driver.find_element(By.XPATH, "//div[@class='el-submenu__title']").click()
        self.driver.find_element(By.XPATH, "//li[@class='el-menu-item']").click()
        self.driver.find_element(By.XPATH, "//i[@class='el-icon-plus']").click()
        time.sleep(1)

    # 保存并提交基本信息
    def bcbtjjbxx(self):
        self.driver.find_elements(By.XPATH, "//button[@class='el-button el-button--info el-button--mini']")[0].click()
        self.driver.find_element(By.XPATH, "//button[@class='el-button el-button--primary el-button--mini']/span[text()='提交']").click()

    # 保存并提交订舱信息
    def bcbtjdcxx(self):
        self.driver.find_elements(By.XPATH, "//button[@class='el-button el-button--info el-button--mini']")[1].click()
        self.driver.find_element(By.XPATH, "//button[@class='el-button el-button--primary el-button--mini']/span[text()='订舱确认']").click()

    # 动态匹配下拉框
    def dtppxlk(self, element, number):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(" ")
        str = "//li[@class='el-select-dropdown__item hover']/span[text()='" + element + "']"
        time.sleep(0.5)
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH, str)).perform()
        self.driver.find_element(By.XPATH, str).click()

    # 需要文本输入的动态匹配下拉框
    def wbsrdtppxlk(self, element, number, text):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(text)
        str = "//li[@class='el-select-dropdown__item hover']/span[text()='" + element + "']"
        time.sleep(0.5)
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH, str)).perform()
        self.driver.find_element(By.XPATH, str).click()

    # 非动态匹配下拉框
    def fdtppxlk(self, element, number):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
        str = "//li[@class='el-select-dropdown__item']/span[text()='" + element + "']"
        self.driver.find_element(By.XPATH, str).click()

    # el-input__inner类,纯文本输入框
    def eii_wbsrk(self, text, number):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(text)

    # 时间选择框
    def sjxzk(self, number):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
        self.driver.find_element(By.XPATH, "//td[@class='available today']").click()

    # 需要确认的时间选择框,默认选择此时此刻
    def qr_sjxzk(self, number, sz):
        self.driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
        self.driver.find_elements(By.XPATH, "//button[@class='el-button el-picker-panel__link-btn el-button--default el-button--mini is-plain']")[sz].click()

    # el-textarea__inner类,纯文本输入框
    def eti_wbsrk(self, number, text):
        self.driver.find_elements(By.XPATH, "//textarea[@class='el-textarea__inner']")[number].send_keys(text)

    # 双击获取,业务编号
    def sjhqywbh(self):
        ActionChains(self.driver).double_click(
            self.driver.find_element(By.XPATH, "//input[@class='el-input__inner']")).perform()
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//input[@class='el-input__inner']").send_keys(Keys.CONTROL, "c")
        time.sleep(0.5)

#运行脚本
def script(driver, eii_dist, eti_dict):
    driver.get_driver()
    # driver.sjhqywbh()
    for ele_list in eii_dist.values():
        if ele_list[0] == "动态匹配下拉框":
            driver.dtppxlk(ele_list[1], ele_list[2])
        if ele_list[0] == "文本输入动态匹配下拉框":
            driver.wbsrdtppxlk(ele_list[1], ele_list[2], ele_list[3])
        if ele_list[0] == "非动态匹配下拉框":
            driver.fdtppxlk(ele_list[1], ele_list[2])
        if ele_list[0] == "文本输入框":
            driver.eii_wbsrk(ele_list[1], ele_list[2])
        if ele_list[0] == "时间选择框":
            driver.sjxzk(ele_list[1])
        if ele_list[0] == "需确认的时间选择框":
            driver.qr_sjxzk(ele_list[1], ele_list[2])
    for eti_list in eti_dict.values():
        driver.eti_wbsrk(eti_list[0], eti_list[1])
    driver.bcbtjjbxx()
    driver.bcbtjdcxx()
    driver.quit_driver()

#读取json文件
def csh(path):
    eii_path = path + "\eii.json"
    eti_path = path + "\eti.json"
    with open(eii_path, "r", encoding="utf-8") as f:
        eii_dist = json.load(f)
    with open(eti_path, "r", encoding="utf-8") as f:
        eti_dist = json.load(f)
    return eii_dist, eti_dist

#打印业务编号
def dyywbh(db, sql):
    db = pymysql.connect(host=db['host'], port=db['port'],
                         user=db['user'], password=db['password'],
                         database=db['database'], charset=db['charset'])
    cur = db.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    db.close()
    print(res)