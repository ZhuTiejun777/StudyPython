import requests
import json
import os

Path = os.path.dirname(os.path.abspath(__file__))
PathTestPicture = "C:\\Users\\Administrator\\Desktop\\项目\\测试图片"


def get_lol_picture(path):
    save_path = path + "\英雄联盟皮肤大全"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for num in range(1, 999):
        js_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/" + str(num) + ".js"
        response = requests.get(url=js_url)
        if response.status_code == 404:
            continue
        js_dist = json.loads(response.text)
        path_hero = save_path + "\\" + js_dist['hero']['name']
        os.mkdir(path_hero)
        print("-----------------------")
        print("开始下载", js_dist['hero']['name'], "皮肤")
        for skins in js_dist['skins']:
            try:
                picture = requests.get(skins['mainImg'])
            except:
                continue
            try:
                with open(path_hero + "\\" + skins.get('name') + ".png", "wb") as f:
                    f.write(picture.content)
                print("保存", skins.get('name'), "成功")
            except:
                change_str = "KDA" + skins.get('name')[5:]
                with open(path_hero + "\\" + change_str + ".png", "wb") as f:
                    f.write(picture.content)
                print("保存", change_str, "成功")
    print("爬取完成")


if __name__ == '__main__':
    get_lol_picture(Path)
