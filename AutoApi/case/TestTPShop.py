# 使用 unittest 实现测试
import json
import unittest
import requests
from parameterized import parameterized

import app
from api.LoginAPI import LoginAPI

def read_from_json():
    data = []
    with open(app.ABS_DIR + "/data/login_data.json", "r", encoding='utf-8') as f:
        all = json.load(f)
        print(all)
    #     for vs in all.values():
    #         test_login = vs.get("test_login")
    #         username = vs.get("username")
    #         password = vs.get("password")
    #         verify_code = vs.get("verify_code")
    #         status = vs.get("status")
    #         msg = vs.get("msg")
    #         data.append((test_login,username,password,verify_code,status,msg))
    # return data

# 读取测试数据json文件


# 返回列表

class TestTPshop(unittest.TestCase):

    # 初始化与销毁
    def setUp(self):
        self.session = requests.session()
        self.login = LoginAPI()

    def tearDown(self):
        self.session.close()


    # 测试函数1：测试验证码
    def test_get_verify_code(self):
        response = self.login.get_verify_code(self.session)
        self.assertEqual("image/png",response.headers.get("Content-type"))


    # 测试函数2: 测试登录
    @parameterized.expand([read_from_json()])
    def test_login(self,username,password,verify_code,status,msg):
        print(username,password,verify_code,status,msg)




    def login_succss(self):
        # 登录成功函数，直接写死参数，为了后面查询订单调用
        self.test_get_verify_code()
        response = self.login.login(self.session,"13812345678","123456","8888")

    # def test_order_by_id(self):
    #     # 测试查询订单函数
    #     self.login_succss()
    #     response = self.login.get_order_by_id(self.session)
    #     self.assertIn("我的订单",response.text)
