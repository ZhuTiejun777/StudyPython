from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
# options.add_argument("--disable-images")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https:\\www.baidu.com")


