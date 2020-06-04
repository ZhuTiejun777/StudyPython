from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class TestSelenium(object):

    def __init__(self, url):
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-images")
        self._options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(chrome_options=self._options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get(url)

    def cookies(self, cookies):
        self.driver.get_cookies()
        self.driver.add_cookie(cookies)

    def base(self, number):
        self.driver.back()
        self.driver.forward()
        self.driver.refresh()
        self.driver.execute_script("javascript")
        self.driver.switch_to.window(self.driver.window_handles[number])
        self.driver.get_screenshot_as_file("path")

    def keyboard(self):
        self.driver.find_element_by_xpath("element").send_keys(Keys.SPACE)

    def getelement(self):
        print(self.driver.find_element_by_xpath("element").text)
        print(self.driver.find_element_by_xpath("element").tag_name)
        print(self.driver.find_element_by_xpath("element").get_attribute("id"))
        print(self.driver.find_element_by_xpath("element").get_property("id"))
        print(self.driver.find_element_by_xpath("element").is_selected())
        print(self.driver.find_element_by_xpath("element").is_displayed())

    def element(self):
        self.driver.find_element(By.XPATH,"element").send_keys()
        self.driver.find_element_by_xpath("element").clear()
        self.driver.find_element_by_xpath("element").submit()

    def webdriverwait(self, time):
        WebDriverWait(self.driver, time).until(self.driver.find_element_by_xpath("element")).send_keys("text")
        WebDriverWait(self.driver, time).until(lambda x:x.find_element_by_xpath("element")).click()

    def cutframe(self):
        self.driver.switch_to.frame("element")
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("element"))
        self.driver.switch_to.default_content()

    def alert(self):
        self.driver.switch_to.alert.accept()
        print(self.driver.switch_to.alert.text)
        self.driver.switch_to.alert.dismiss()
        self.driver.switch_to.alert.send_keys("text")

    def select(self):
        Select("element").select_by_index("number")

    def action(self):
        ActionChains(self.driver).move_to_element("element").perform()

    def quitdriver(self):
        self.driver.close()
        self.driver.quit()

