import requests


import app


class Login:

    def __init__(self):
        self.verify_code_url = app.BASE_URL + "/app/v1_0/sms/codes/"
        self.login_url = app.BASE_URL + "/app/v1_0/authorizations"

    # 获取验证码函数
    def get_verify_code(self, mobile):
        # 发送验证码请求并返回响应结果
        return requests.get(self.verify_code_url + mobile)

    # 登录函数
    def login(self, mobile, code):
        myJson = {}
        if mobile:
            myJson["mobile"] = mobile
        if code:
            myJson["code"] = code
        print(myJson)
        return requests.post(self.login_url,json=myJson)
    #
    # def login(self, mobile, code):
    #     # 判断提交数据
    #     myJson = {}
    #     #None 判断
    #     if mobile:
    #         myJson["mobile"] = mobile
    #     if code:
    #         myJson["code"] = code
    #     print(myJson)
    #     return requests.post(self.login_url,json=myJson)
