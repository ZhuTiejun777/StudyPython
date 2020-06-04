import json
import unittest

import app
from parameterized import parameterized
from api.LoginAPI import Login


def read_from_json():
    data = []
    with open(app.BASE_DIR + "/data/login_case.json", "r", encoding="utf-8") as f:
        data_json = json.load(f)
    for ele in data_json.values():
        data.append((ele.get("mobile"),
                     ele.get("code"),
                     ele.get("status_code"),
                     ele.get("message")))
    return data



class TestLogin(unittest.TestCase):
    def setUp(self):
        # 获取Login对象
        self.login = Login()

    # 测试函数1:测试短信验证码
    def test01_get_verify_code(self):
        result = self.login.get_verify_code("13477639883")
        print(result.status_code)
        print(result.json())

    # 测试函数2:测试登录 -- 数据动态导入参数化
    @parameterized.expand(read_from_json)
    def test02_login(self,mobile,code,status_code,message):
        res = self.login.login(mobile,code)
        print(res.text)
        self.assertEqual(status_code,res.status_code)
        self.assertIn(message,res.text)


        # 断言状态码

        # 断言响应体
    def test03_login_success(self):
        response = self.login.login("13477639883","429440")
        app.TOKEN = response.json().get("data").get("token")
        # 先执行获取验证码 -- 再手动输入验证码执行登录成功用例
        self.assertIn("OK",response.text)
        self.assertEqual(201,response.status_code)

        # 提取tokie后复制给公共常量

        # 断言状态码

        # 断言响应体

