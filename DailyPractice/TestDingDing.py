import requests

URL = "https://oapi.dingtalk.com/robot/send?access_token=ccaaba27b57ed7e2abec0c3e8651634daaaedf84cc71a01576d17c43c4da7ff6"

jsonText = {
    "msgtype": "text",
    "text": {
        "content": "http://192.168.3.192/newDzka/QA/Defect/List    test"
    },
    "at": {
        "atMobiles": [
        ],
        "isAtAll": False
    }
}

response = requests.post(url=URL, json=jsonText)
print(response.status_code)
print(response.text)