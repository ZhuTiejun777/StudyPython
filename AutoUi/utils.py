# 保证浏览器驱动对象只有一个
import json
import time

import config
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# 工具方法 -- 读取测试数据文件
def exist_text(text):
    try:
        xpath = "//*[contains(text(),'{}')]".format(text)
        element = DriverUtil.get_driver().find_element_by_xpath(xpath)
        return element is not None
    except:
        print("current page is not contains[{}]".format(text))
        return False


def load_test_data(file_name):
    with open(config.BASE_DIR + "\data\\" + file_name, encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data


# 工具方法 -- 切换到新窗口
def switch_to_window():
    time.sleep(5)
    driver = DriverUtil.get_driver()
    driver.switch_to.window(driver.window_handles[-1])


# 方法工具 -- 截图
def screenshot():
    screenshot_path = config.BASE_DIR + "/screenshot/{}.png".format(time.strftime("%Y%m%d%H%M%S"))
    DriverUtil.get_driver().get_screenshot_as_file(screenshot_path)


# 工具方法--判断页面是否存在指定文本内容 -- 参数-判断内容 -- 返回布尔结果


class DriverUtil:
    # 定义类属性保存驱动对象
    _driver = None
    # 定义标记,判断是否需要退出驱动对象
    _auto_quit = True

    # 获取浏览器驱动对象  类方法
    @classmethod
    def get_driver(cls):
        # 判断_driver中是否存有驱动,如果没有实例化一个保存在_driver中
        if cls._driver is None:
            cls._driver = webdriver.Chrome()
            cls._driver.maximize_window()
            cls._driver.implicitly_wait(10)
        # 返回_driver中的驱动对象
        return cls._driver


    #无头浏览器
    # @classmethod
    # def get_driver(cls):
    #     if cls._driver is None:
    #         options = Options()
    #         options.add_argument('--headless')
    #         options.add_argument('--disable-gpu')
    #         path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    #         cls._driver = webdriver.Chrome(executable_path=path,chrome_options=options)
    #     return cls._driver


    #无头浏览器
    # @classmethod
    # def get_driver(cls):
    #     if cls._driver is None:
    #         co = webdriver.ChromeOptions()
    #         co.headless = True
    #         cls._driver = webdriver.Chrome(options=co)
    #     return cls._driver



    # 退出浏览器驱动对象 类方法
    @classmethod
    def quit_driver(cls):
        # 如果_driver属性中有驱动对象,退出驱动对象-重置为None
        if cls._auto_quit and cls._driver is not None:
            cls._driver.quit()
            cls._driver = None

    # 手动设置自动退出
    @classmethod
    def set_auto_quit(cls, auto_quit):
        cls._auto_quit = auto_quit
