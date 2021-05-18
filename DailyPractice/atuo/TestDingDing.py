import base64
import hashlib
import hmac
import time
import urllib.parse

import requests
secret = "SECe4b8a7e856a992b77c73407e051d3bb6431ab7322151680b9bb481128e3b81c8"

header = {
    "Content-Type": "application/json;charset=UTF-8"
}

timestamp = str(round(time.time() * 1000))
stringToSign = timestamp + "\n" + secret
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

#URL = "https://oapi.dingtalk.com/robot/send?access_token=" + secret + "&timestamp=" + timestamp + "&sign=" + sign
#print(URL)
URL = "https://oapi.dingtalk.com/robot/send?access_token=ed68cd6983c5c0c65ad8462f39af1bf2f1b3206aa1c79f79f960aa9b78cb45cd"

jsonText = {
    "msgtype": "text",
    "text": {
        "content": "http://192.168.66.179:8082/"
    },
    "at": {
        "atMobiles": [
        ],
        "isAtAll": False
    }
}

response = requests.post(url=URL, headers=header, json=jsonText)
print(response.status_code)
print(response.text)