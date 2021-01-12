import time

from selenium import webdriver

def __init__(self, url):
    self._options = webdriver.ChromeOptions()
    self._options.add_argument("--no-sandbox")
    self._options.add_argument("--disable-images")
    self._options.add_argument('--blink-settings=imagesEnabled=false')
    self.driver = webdriver.Chrome(chrome_options=self._options)
    self.driver.maximize_window()
    self.driver.implicitly_wait(30)
    self.driver.get(url)


#options = webdriver.ChromeOptions()
#driver = webdriver.Chrome(chrome_options=options)
#driver.maximize_window()
#driver.implicitly_wait(30)
#driver.get("https://www.baidu.com")


driver = webdriver.Chrome("/Users/tiejunzhu/Desktop/profile/chromedriver")
driver.get('http://www.baidu.com')
driver.maximize_window()
driver.implicitly_wait(30)
driver.find_element_by_xpath("//input[@id='kw']").send_keys("test")
driver.find_element_by_xpath("//input[@id='su']").click()
time.sleep(10)
driver.close()
