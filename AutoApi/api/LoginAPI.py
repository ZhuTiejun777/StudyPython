

class LoginAPI:

    def __init__(self):
        self.get_verify_code_url = "http://localhost/index.php?m=Home&c=User&a=verify"
        self.login_url = "http://localhost/index.php?m=Home&c=User&a=do_login"
        self.get_order_by_id_url = "http://localhost/Home/Order/order_list.html"

    # 封装获取验证码接口，返回响应体
    def get_verify_code(self,session):
        response = session.get("http://localhost/index.php?m=Home&c=User&a=verify")
        return response






    def login(self,session,username,password,verify_code):
        myData={
            "username": username,
            "password": password,
            "verify_code":verify_code
        }
        response = session.post(self.login_url,data=myData)
        return response

    def get_order_by_id(self,session):
        response = session.get(self.get_order_by_id_url)
        return response