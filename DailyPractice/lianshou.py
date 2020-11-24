import os
import re
import time
from urllib import parse

import pyecharts
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options




# path = os.path.abspath(os.path.dirname(__file__))
# url ='https://www.52bqg.com/book_11276/5824305.html'
#
# options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-images")
# options.add_argument('--blink-settings=imagesEnabled=false')
# driver = webdriver.Chrome(chrome_options=options)
# driver.maximize_window()
# driver.implicitly_wait(30)
# driver.get(url)
#
# ebook_name = driver.find_element(By.XPATH,"//a[@href='https://www.52bqg.com/book_11276/']").text
# if not os.path.exists(path + "\\e-book"):
#     os.mkdir(path + "\\e-book")
# ebook_path = path + "\\e-book\\" + ebook_name + ".txt"
# file = open(ebook_path,"w",encoding="utf-8")
#
# while True:
#     print(driver.find_element(By.XPATH,"//div[@class='bookname']/h1").text)
#     file.write(driver.find_element(By.XPATH,"//div[@class='bookname']/h1").text)
#     file.write("\n")
#     file.write("\n")
#     file.write("\n")
#     print(driver.find_element(By.XPATH, "//div[@id='content']").text)
#     file.write(driver.find_element(By.XPATH, "//div[@id='content']").text)
#     file.write("\n")
#     file.write("\n")
#     file.write("-" * 100 )
#     file.write("\n")
#     file.write("\n")
#     driver.find_element(By.XPATH,"//a[text()='下一章']").click()


# path = os.path.abspath(os.path.dirname(__file__))
# ebook_name = 'tt'
# ebook_path = path + "\\" + ebook_name + ".txt"
# file = open(ebook_path,'w')
# file.write("aaaa")
# file.write("aa")
#
#
# Path = os.path.dirname(os.path.abspath(__file__))

# dirver = webdriver.Firefox()
# dirver.get("http://www.y80s.com/movie/11729")
# dirver.maximize_window()
# dirver.implicitly_wait(10)
# ele_download = dirver.find_element(By.XPATH, "//a[text()='本地下载']")
# print(ele_download.get_attribute("href"))
# dirver.close()

# a = "http://xunleib.zuida360.com/1804/X%E6%88%98%E8%AD%A6%EF%BC%9A%E9%80%86%E8%BD%AC%E6%9C%AA%E6%9D%A5.BD1280%E9%AB%98%E6%B8%85%E7%89%B9%E6%95%88%E4%B8%AD%E8%8B%B1%E5%8F%8C%E5%AD%97%E7%89%88.mp4"
# url = parse.unquote(a)
# print(url)
# response = requests.get(url)


# driver = webdriver.Firefox()
# driver.get("https:www.baidu.com")
# time.sleep(3)
# driver.get("https:www.baidu.com")
# driver.close() a():
# def a():
#     for num in range(1, 2):
#         print(num-1)
#         print(num*3-3)
#         print(num*3-2)
#         print(num*3-1)
#     return
# for num in range(1, 2):
#     print(num-1)
#     print(num*3-3)
#     print(num*3-2)
#     print(num*3-1)

# str = "(10000)"
#
#
# print(int(re.search("[0-9]\d*", str).group()))


# class PortNameSpider(object):
#
#     def __init__(self, url):
#         self.driver = webdriver.Firefox()
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(10)
#         self.driver.get(url)
#         self.port_list = []
#
#     def portnamespider(self, num):
#         for i in range(0, num):
#             ele_num = self.driver.find_elements(By.XPATH, "//td[@height='24']")[i].text
#             self.driver.find_elements(By.XPATH, "//td[@height='24']/a[@target='_blank']")[i].click()
#             port_num = int(re.search("[0-9]\d*", ele_num).group())
#             print(port_num)
#             for i in range(1, port_num + 1):
#                 gkdm = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#F5F5F5']/a[@target='_blank']")[i - 1].text
#                 gkmc = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 3].text
#                 szgj = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 2].text
#                 hx = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 1].text
#                 print(gkdm, gkmc, szgj, hx)
#                 self.port_list.append([gkdm, gkmc, szgj, hx])
#             self.driver.close()
#         print(self.port_list)
#         self.driver.quit()
#         return self.port_list


# list_date = [
#     ["a","b","c","d"],
#     ["f","q","z","m"],
#     ["n","b","v","u"]
# ]
#
# def writetext(path, list):
#     text_path = path + "\port.text"
#     if os.path.exists(text_path):
#         os.remove(text_path)
#     with open(text_path, "w+", encoding="utf-8") as f:
#         for list1 in list:
#             f.write(list1[0] + " ")
#             f.write(list1[1] + " ")
#             f.write(list1[2] + " ")
#             f.write(list1[3] + "\n")
# writetext(Path, list_date)

# str = "英雄港（ANGRA DO HEROISMO）"

# print(type(list1[0]))
# print(list1[0])
# print(str.split("（")[0])

# print(str.split("（")[0])
# print(str.split("（")[1][:-1])



# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
#
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.get("https://gangkou.51240.com/")

# def testportspider(self, list, path):
#     text_path = path + "\port.text"
#     if os.path.exists(text_path):
#         os.remove(text_path)
#     for tuple in list:
#         area, num = tuple
#         url = "https://gangkou.51240.com/" + area + "__gangkousou"
#         self.driver.get(url)
#         for i in range(1, num + 1):
#             gkdm = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#F5F5F5']/a[@target='_blank']")[i - 1].text
#             gkmc = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 3].text
#             szgj = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 2].text
#             hx = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")[i * 3 - 1].text
#             with open(text_path, "w+", encoding="utf-8") as f:
#                 f.write(gkdm + " ")
#                 f.write(gkmc + " ")
#                 f.write(szgj + " ")
#                 f.write(hx + "\n")
#             print(gkdm, gkmc, szgj, hx)
#             self.list.append([gkdm, gkmc, szgj, hx])
#     print(self.list)
#     self.driver.quit()
#     return self.list

# def __init__(self, url, path):
#     self._options = webdriver.ChromeOptions()
#     self._options.add_argument('--headless')
#     self._options.add_argument('--disable-gpu')
#     self._options.add_argument('--no-sandbox')
#     self._options.add_argument('--start-maximized')
#     self._options.add_argument('--blink-settings=imagesEnabled=false')
#     self.driver = webdriver.Chrome(executable_path=path, chrome_options=self._options)
#     self.driver.implicitly_wait(10)
#     self.driver.get(url)
#     self.list = []


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# path = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python37\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=path,chrome_options=options)
# driver.get("https:www.baidu.com")
# driver.find_element(By.ID, "kw").send_keys("测试")
# driver.find_element(By.ID, "su").click()
# path1 = os.path.dirname(os.path.abspath(__file__)) + "\\test.png"
# print(path1)
# time.sleep(3)
# driver.get_screenshot_as_file(path1)
# driver.quit()

# options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(chrome_options=options)
# driver.maximize_window()
# driver.implicitly_wait(10)
# driver.get("https:www.baidu.com")
# time.sleep(5)


