import requests
import os
import json

# Path = os.path.dirname(os.path.abspath(__file__))+ "\英雄联盟皮肤大全"



# str1 = {"ZZ":"K/DA 卡莎 至臻"
#         }
# change_str = "KDA" + str1.get('ZZ')[5:]
# print(change_str)


# with open("xzjbxx.json", "w") as f:
#     f.write("sss")
#     f.close()


# pf_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/1.js"
#
# response = requests.get(url=pf_url)
#
# js_dist = json.loads(response.text)
#
# path_hero = Path + "\\" +js_dist['hero']['name']
#
# print(path_hero)

#
# picture = requests.get("https://game.gtimg.cn/images/lol/act/img/skin/big1010.jpg")
#
# # with open(Path + "\\黑暗之女\\" + "安妮" + ".png", "wb") as f:
# with open("C:\\Users\\Administrator\\Desktop\\项目\\世晨\\script\\英雄联盟皮肤大全\\痛苦之拥\\" + "K/DA 伊芙琳.png", "wb") as f:
#     f.write(picture.content)
#
# print(Path + "\\黑暗之女\\" + "安妮" + ".png")

# dict1 = {
#     "zz":"123",
#     "xx":"456",
#     "cc":"789"
# }
# print(dict1['zz'])
# print(dict1.get('zz'))


#
# pf_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/1.js"
#
# response = requests.get(url=pf_url)

# json_d = str(json.loads(response.text))
#
# # print(response.text)
# print(json_d)
#
#
# url_list = re.findall("'mainImg': 'https://[\S]*jpg'",json_d)
#
#
#
# for i in url_list:
#     print(i)
#
# js_dist = json.loads(response.text)
#
# # print(js_dist['hero']['name'])
#
#
# for skins in js_dist['skins']:
#     print(skins['name'])
#     print(skins['mainImg'])

# test_url = "https://game.gtimg.cn/images/lol/act/img/skin/big1010.jpg"
#
# picture = requests.get(test_url)
# # print(picture.content)
# with open(Path + "\CESHI" +"\.jpg", "wb") as f:
#     f.write(picture.content)



# for num in range(1,140):
#     print(num)
#     js_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/" + str(num) + ".js"
#     res = requests.get(js_url)
#     print(res.status_code)
#     print(js_url)



