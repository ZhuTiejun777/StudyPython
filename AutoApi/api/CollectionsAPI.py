import requests

import app


class Collections:
    def __init__(self):
        self.save_url = app.BASE_URL + "/app/v1_0/article/collections"

    def save(self, id, token):
        # 提交数据
        myJson = {"target":id}
        myHeaders = {"Content-Type":"application/json","Authorization":"Bearer "+token}
        return requests.post(self.save_url,json=myJson,headers=myHeaders)
        # 构造请求头,传入token
		# {"Content-Type":"application/json","Authorization":"Bearer TOKEN的值"}
        # 发送请求,返回响应

    def cancel(self, id, token):
        # 构造请求头,传入token
        myHeaders = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        return requests.delete(self.save_url+"/"+str(id),headers=myHeaders)
        # 构造请求头,传入token