from selenium import webdriver
from selenium.webdriver.common.by import By
import os

path = os.path.abspath(os.path.dirname(__file__))

url = "https://read.qidian.com/chapter/bc130qp2-qb36JmDw--oJQ2/eSlFKP1Chzg1"
chromedriverPath = "/Users/tiejunzhu/Desktop/profile/chromedriver"
num = 0

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-images")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options, executable_path=chromedriverPath)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(url)
driver.find_element(By.XPATH,"//a[@class='lbf-panel-close lbf-icon lbf-icon-close']").click()
ebook_name = driver.find_element(By.XPATH,"//a[@id='bookImg']").text
if not os.path.exists(path + "/e-book"):
    os.mkdir(path + "/e-book")
ebook_path = path + "/e-book/" + ebook_name + ".txt"
print(ebook_path)
file = open(ebook_path,"w",encoding="utf-8")

while True:
    try:
        text = driver.find_element(By.XPATH,"//h3[@class='lang']").get_attribute("text")
        if text == "需要订阅后才能阅读":
            break
    except:
        print(50 * "-")
    while True:
        try:
            driver.find_elements(By.XPATH, "//span[@class='content-wrap']")[num]
        except:
            print(50 * "-")
            file.write(50 * "-" + "\n")
            num = 0
            break
        if num == 0:
            print(driver.find_elements(By.XPATH, "//span[@class='content-wrap']")[num].text)
            file.write(driver.find_elements(By.XPATH, "//span[@class='content-wrap']")[num].text + "\n")
        else:
            print(driver.find_elements(By.XPATH, "//span[@class='content-wrap']")[num].text)
            file.write(driver.find_elements(By.XPATH, "//span[@class='content-wrap']")[num].text + "\n")
        num += 1
    driver.find_element(By.XPATH,"//a[@id='j_chapterNext']").click()

driver.quit()


