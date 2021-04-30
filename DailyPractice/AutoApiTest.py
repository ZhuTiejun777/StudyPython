import json

import requests

urlLogin = "http://192.168.66.178:8080/AutoWeb/login"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "JSESSIONID=382A4CF200A1388EB31B7E3279FD93D3; jenkins-timestamper-offset=-28800000; iconSize=32x32",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}

dates = {
    "username": "zhutj25764",
    "password": "1098738134Ztj"
}

session = requests.Session()

response = session.post(url=urlLogin, headers=headers, data=dates)


print(response.text)
print(response.status_code)
print(response.headers)
print(response.cookies)




def runCasePlan():
    url = "http://192.168.66.178:8080/AutoWeb/runCasePlan"
    headersTest = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "JSESSIONID=148FAC7FAA4DC8021BD1ADAF7AB35BE9; jenkins-timestamper-offset=-28800000; iconSize=32x32"
    }
    params = {
        "versionId": "221328054968909824",
        "planIdList": ["228572068440965120"]
    }
    responseTest = requests.post(url=url, headers=headersTest, data=json.dumps(params))

    print(responseTest.text)
    print(responseTest.status_code)
    print(responseTest.headers)

