# Author:jiangnan
# _*_coding:utf-8_*_
# 2020/10/28  14:00

# 编写装饰器，为多个函数加上认证的功能(用户的账号密码来源于文件),要求登录成功一次，后续的函数都无需再输入用户名和密码

# with open('user.txt') as f:
#     users = eval(f.read())

users = {"user":"1","pwd":"1","token":False}

def login_check(func):
    '''
    登录验证的装饰器
    :param func:
    :return:
    '''
    def ado():
        # print(users["token"])
        # print(func)
        # print("函数外部-----------")
        if not users['token']:  # 判断token值是否为False
            # print(users["token"])
            # print(func)
            # print("函数内部if-----------")
            print('------登录页面------')
            username = input('账号：')
            password = input('密码：')
            #  登录校验
            if users["user"] == "1" and users["pwd"] == "1":
                users['token'] = True  # 修改token值
                func()  # 调用被装饰器的函数
        else:
            # print(users["token"])
            # print(func)
            # print("函数内部else-----------")
            func()  # token值为 True直接调用函数
    return ado


@login_check
def index():
    print('首页登录了')


@login_check
def page1():
    print('page页面登录了')


if __name__ == '__main__':
    index()
    page1()