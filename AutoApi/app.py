# 封装程序常量
import os
# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)


# 默认URL
BASE_URL = "http://ttapi.research.itcast.cn"


# 用户token
TOKEN = None

ABS_PATH = os.path.abspath(__file__)
print(ABS_PATH)
ABS_DIR = os.path.dirname(ABS_PATH)
print(ABS_DIR)