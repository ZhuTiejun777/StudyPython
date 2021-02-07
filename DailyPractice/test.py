# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# import time
# import pymysql
# import re
#

member = 14
str = "sed -i 's/member:7/member:%d/g' /etc/kubernetes/yaml/etc/kwl-member.yaml" % member
#print(str)

strformat = "sed -i 's/member:7/member:{0}/g' /etc/kubernetes/yaml/etc/kwl-member.yaml".format(member)
#print(strformat)

replaceCommand = "/etc/kubernetes/yaml/etc/applymember.sh {0}".format(member)
print(replaceCommand)
# db = pymysql.connect(host="192.168.3.110",port=3306,
#                        user="root",password="zjport",
#                        database="tsn",charset="utf8")
# cur = db.cursor()
# sql = "select business_no from tsn_shipping_export_base order by id desc limit 1"
# cur.execute(sql)
# res = cur.fetchall()
# # bh = re.findall("\w*",res)
# cur.close()
# db.close()
# print(res)
#
#
# # cookies = {
# #     "userName": "%E4%B8%96%E6%99%A8%E7%AE%A1%E7%90%86%E5%91%98",
# #     "userId": "sc_admin",
# #     "login_token": "623f29f1-335e-4f2f-b3a3-63fb83adeafb"
# # }
# # driver.add_cookie({'name': 'userName', 'value': cookies['userName']})
# # driver.add_cookie({'name': 'userId', 'value': cookies['userId']})
# # driver.add_cookie({'name': 'login_token', 'value': cookies['login_token']})
#
#
# # 定位存在问题
# '"ele_jsdw": ["文本输入动态匹配下拉框", "纸箱", 24, "CT"],'
#
# url = 'http://122.224.230.26:20054/login'
# cookies = {
#     "name": "login_token",
#     "value": "623f29f1-335e-4f2f-b3a3-63fb83adeafb"
# }
# # el-input__inner类元素定位
# ele_eii = {
#     "ele_khdm": ["QS001A | 安吉博扬家具有限公司", 1],
#     "ele_ywlx": ["海运整箱", 2],
#     "ele_fhr": ["QS001A | 安吉博扬家具有限公司", 3],
#     "ele_khbh": ["QS001A", 4],
#     "ele_ystk": ["CY-CY", 5],
#     "ele_yftk": ["PREPAID（预付）", 6],
#     "ele_qyg": ["ningbo1", 7, "宁波"],
#     "ele_qymt": ["9", 8],
#     "ele_zzg": ["Road bay", 9],
#     "ele_xhg": ["Cai mep", 10],
#     "ele_ckka": ["宁波(NB)", 11],
#     "ele_shd": ["测试基本信息收货地", 12],
#     "ele_mdd": ["测试基本信息目的地", 13],
#     "ele_dcdl": ["订舱代理代码 | 订舱代理名称", 14],
#     "ele_yjcq": [15, 0],
#     "ele_tdlx": ["ORIGINAL B/L", 16],
#     "ele_tdfs": ["5", 17],
#     "ele_qfd": ["测试基本信息签发地", 18],
#     "ele_xx": ["40GP | 40GP", 19],
#     "ele_xl": ["5", 20],
#     "ele_zwpm": ["测试基本信息中文品名", 21],
#     "ele_ywpm": ["CSJBXXYWPM", 22],
#     "ele_mt": ["测试基本信息唛头", 23],
#     "ele_js": ["5", 24],
#     "ele_jsdw": ["袋", 25],
#     "ele_mz": ["5", 26],
#     "ele_tj": ["5", 27],
#     "ele_dcbh": ["DCXXDCBH", 28],
#     "ele_MBL": ["DCXXMBL", 29],
#     "ele_HBL": ["DCXXHBL", 30],
#     "ele_cgs": ["IRISL | 伊朗航运", 31],
#     "ele_S/Obh": ["S/Obianhao", 32],
#     "ele_S/Oyxq": [33, 30],
#     "ele_cm": ["cscm", 34],
#     "ele_hc": ["cshc", 35],
#     "ele_kgrq": [36],
#     "ele_jgangrq": [37],
#     "ele_jguanrq": [38],
#     "ele_jdrq": [39],
#     "ele_ETD": [40],
#     "ele_ATD": [41],
#     "ele_yxsq": ["订舱信息用箱申请", 42],
#     "ele_hx": ["SDFS | 艾欧尼亚", 43]
# }
#
# # el-textarea__inner类元素定位
# ele_eti = {
#     "ele_shr": ["测试基本信息收货人", 1],
#     "ele_tzr": ["测试基本信息通知人", 2],
#     "ele_jbxxbz": ["测试基本信息备注", 3],
# }
#
#
# # 初始化加载页面，进入新增界面
# def get_driver(url, cookie):
#     driver = webdriver.Firefox()
#     driver.maximize_window()
#     driver.implicitly_wait(30)
#     driver.get(url)
#     driver.add_cookie(cookie_dict=cookie)
#     driver.refresh()
#     driver.find_element(By.XPATH, "//div[@class='el-submenu__title']").click()
#     driver.find_element(By.XPATH, "//li[@class='el-menu-item']").click()
#     driver.find_element(By.XPATH, "//i[@class='el-icon-plus']").click()
#     time.sleep(1)
#     return driver
#
#
# # 保存并提交基本信息
# def bcbtjjbxx(driver):
#     driver.find_element(By.XPATH, "//button[@class='el-button el-button--info el-button--mini']").click()
#     time.sleep(1)
#     driver.find_element(By.XPATH,
#                         "//button[@class='el-button el-button--primary el-button--mini']/span[text()='完成并提交']").click()
#     time.sleep(1)
#
#
# # 动态匹配下拉框
# # 1、3、8、9、14、19、25、31、43、
# def dtppxlk(driver, number, element):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(" ")
#     time.sleep(1)
#     str = "//li[@class='el-select-dropdown__item']/span[text()='" + element + "']"
#     driver.find_element(By.XPATH, str).click()
#
#
# # 需要文本输入的动态匹配下拉框
# # 7、
# def wbsrdtppxlk(driver, number, element, text):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(text)
#     time.sleep(1)
#     str = "//li[@class='el-select-dropdown__item']/span[text()='" + element + "']"
#     driver.find_element(By.XPATH, str).click()
#
#
# # 非动态匹配下拉框
# # 2、5、6、11、16、
# def fdtppxlk(driver, number, element):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
#     str = "//li[@class='el-select-dropdown__item']/span[text()='" + element + "']"
#     driver.find_element(By.XPATH, str).click()
#
#
# # el-textarea__inner类,纯文本输入框
# # 1、2、3、
# def eti_wbsrk(driver, number, text):
#     driver.find_elements(By.XPATH, "//textarea[@class='el-textarea__inner']")[number].send_keys(text)
#
#
# # el-input__inner类,纯文本输入框
# # 4、12、13、18、20、21、22、23、24、26、27、28、29、30、32、34、35、42、
# def eii_wbsrk(driver, number, text):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].send_keys(text)
#
#
# # 时间选择框
# # 15、33、
# def sjxzk(driver, number, date):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
#     driver.find_elements(By.XPATH, "//td[@class='available']")[date + 1].click()
#
#
# # 需要确认的时间选择框,默认选择此时此刻
# # 36、37、38、39、40、41、
# def qr_sjxzk(driver, number):
#     driver.find_elements(By.XPATH, "//input[@class='el-input__inner']")[number].click()
#     driver.find_elements(By.XPATH,
#                          "//button[@class='el-button el-picker-panel__link-btn el-button--text el-button--mini']")[
#         5].click()
#
#
# #ActionChains(driver).move_to_element().perform()

businessNo = "s"

url_zcdcxx = "http://122.224.230.26:20054/tsnShipping/shipping/export/input/saveTransportInfo?businessNo=" + businessNo


print(url_zcdcxx)
