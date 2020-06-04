import requests
import app


class Articles:

    def __init__(self):
        self.articles_by_channle_id_url = app.BASE_URL + "/app/v1_0/articles"

    # 获取频道函数
    def get_articles_by_channle_id(self, channel_id):
        myJson = {"channel_id":channel_id}
        # 发送获取频道请求并返回响应结果
        return requests.get(self.articles_by_channle_id_url,json=myJson)
