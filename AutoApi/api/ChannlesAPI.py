import app
import requests


class Channles:

    def __init__(self):
        self.channles_url = app.BASE_URL + "/app/v1_0/channels"
    # 获取频道函数
    def get_channles(self):
        # 发送获取频道请求并返回响应结果
        return requests.get(self.channles_url)
