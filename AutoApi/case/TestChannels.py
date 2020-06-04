import unittest

from api.ChannlesAPI import Channles


class TestLogin(unittest.TestCase):
    def setUp(self):
        # 获取Channles对象
        self.channles = Channles()

    # 测试函数1:测试获取所有频道列表
    def test01_get_channles(self):
        response = self.channles.get_channles()
        self.assertEqual("OK",response.json().get("message"))
        # 断言状态码

