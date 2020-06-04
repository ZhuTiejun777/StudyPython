import unittest

import app

from api.CollectionsAPI import Collections


class TestCollections(unittest.TestCase):

    def setUp(self):
        self.collections = Collections()

    # 先登录在收藏 -- token 令牌
    # 服务器开辟的存储空间需要使用token去认证访问
    # 关联实现 取token 用token
    # 1. 从登陆响应结果中提取token
    # 2. 收藏请求提交时携带token
    def test01_save(self):
        response = self.collections.save(2,app.TOKEN)
        self.assertEqual(201,response.status_code)
        self.assertIn("OK",response.json().get("message"))

    def test02_cancel(self):
        response = self.collections.cancel(2,app.TOKEN)
        self.assertEqual(204,response.status_code)
