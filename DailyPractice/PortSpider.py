import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

port_url = "https://gangkou.51240.com/"
driver_path = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python37\chromedriver.exe"
Path = os.path.dirname(os.path.abspath(__file__))


class GetPortName(object):

    def __init__(self, url):
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-images")
        self._options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(chrome_options=self._options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get(url)
        self.list = []

    def getportelement(self, num):
        ele_num = self.driver.find_elements(By.XPATH, "//td[@height='24']")
        ele_port = self.driver.find_elements(By.XPATH, "//td[@height='24']/a[@target='_blank']")
        for i in range(0, num):
            num = ele_num[i].text
            port = ele_port[i].text
            print(port, int(re.search("[0-9]\d*", num).group()))
            self.list.append([port, int(re.search("[0-9]\d*", num).group())])
        self.driver.quit()
        return self.list

    def writetext(self, path, list):
        text_path = path + "\date.text"
        if os.path.exists(text_path):
            os.remove(text_path)
        with open(text_path, "w+", encoding="utf-8") as f:
            for temp_list in list:
                f.write(temp_list[0] + " ")
                f.write(str(temp_list[1]) + "\n")


class PortSpider(object):

    def __init__(self):
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-images")
        self._options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(chrome_options=self._options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.list = []

    def portspider(self, list):
        for tuple in list:
            area, num = tuple
            url = "https://gangkou.51240.com/" + area + "__gangkousou"
            self.driver.get(url)
            gkdm_driver = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#F5F5F5']/a[@target='_blank']")
            gkmc_driver = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")
            szgj_driver = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")
            hx_driver = self.driver.find_elements(By.XPATH, "//td[@bgcolor='#FFFFFF']")
            for i in range(1, num + 1):
                gkdm = gkdm_driver[i - 1].text
                gkmc = gkmc_driver[i * 3 - 3].text
                szgj = szgj_driver[i * 3 - 2].text
                hx = hx_driver[i * 3 - 1].text
                print(gkdm, gkmc, szgj, hx)
                self.list.append([gkdm, gkmc, szgj, hx])
        self.driver.quit()
        return self.list

    def writetext(self, path, list):
        text_path = path + "\port.text"
        if os.path.exists(text_path):
            os.remove(text_path)
        with open(text_path, "w+", encoding="utf-8") as f:
            for temp_list in list:
                f.write(temp_list[0] + " ")
                f.write(temp_list[1].split("（")[0] + " ")
                f.write(temp_list[1].split("（")[1][:-1] + " ")
                f.write(temp_list[2] + " ")
                f.write(temp_list[3] + "\n")


getportname = GetPortName(port_url)
data_list = getportname.getportelement(34)
getportname.writetext(Path, data_list)

portspider = PortSpider()
port_list = portspider.portspider(data_list)
portspider.writetext(Path, port_list)
