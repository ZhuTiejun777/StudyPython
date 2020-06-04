import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

url = "http://122.224.230.26:20054/login"

cookies = {
    "name": "login_token",
    "value": "0bd4ea72-86e1-4ad3-85f2-2fa3a61468f5"
}


class PictureDiscern():

    def __init__(self, url, cookies):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get(url=url)
        self.driver.add_cookie(cookie_dict=cookies)
        self.driver.refresh()
        time.sleep(2)

    def accessdispatch(self, businessno):
        self.driver.find_elements(By.XPATH,"//li[@role='menuitem']")[2].click()
        time.sleep(2)
        self.driver.find_elements(By.XPATH,"//input[@placeholder='请输入搜索内容']")[0].send_keys(businessno)
        time.sleep(2)
        self.driver.find_elements(By.XPATH,"//button[@type='button']")[0].click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,"//span[text()='SETEST20031600002']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,"//span[text()='图片识别']").click()
        time.sleep(2)

    def uploadingpicture(self):
        self.driver.find_elements(By.XPATH,"//input[@name='file']")[0].send_keys("C:\\Users\\Administrator\\Desktop\\箱号\\微信图片_20200316091759.jpg")
        time.sleep(2)
        self.driver.find_elements(By.XPATH,"//input[@name='file']")[1].send_keys("C:\\Users\\Administrator\\Desktop\\箱号\\8.26J4.jpg")
        time.sleep(2)
        self.driver.find_element(By.XPATH,"//span[text()='识 别']").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,"//span[text()='确 定']").click()
        time.sleep(2)

    def quitdriver(self):
        self.driver.quit()


pd = PictureDiscern(url, cookies)
pd.accessdispatch("SETEST20031600002")
pd.uploadingpicture()