import unittest

from api.ArticlesAPI import Articles


class TestArticles(unittest.TestCase):
    def setUp(self):
        # 获取Articles对象
        self.articles = Articles()

    # 测试函数1:测试获取指定频道所有文章
    def test01_get_articles_by_channle_id(self):
        res = self.articles.get_articles_by_channle_id(2)
        print(res.text)
        # 断言结果
        self.assertEqual("OK",res.json().get("message"))

