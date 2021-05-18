# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/04/14"

import json

import jsonpath
import requests

urlLogin = "http://192.168.66.178:8080/AutoWeb/login"
urlCasePlen = "http://192.168.66.178:8080/AutoWeb/runCasePlan"
urlCountResult ="http://192.168.66.178:8080/AutoWeb/getReport?planId=228572068440965120"


headersForm = {
    "Content-Type": "application/x-www-form-urlencoded"
}
headersJson = {
    "Content-Type": "application/json;charset=UTF-8"
}

dates = {
    "username": "zhutj25764",
    "password": "1098738134Ztj"
}
paramsCasePlen = {
    "versionId": "221328054968909824",
    "planIdList": ["228572068440965120"]
}
paramsCountResult = {
    "planId": "228572068440965120"
}

session = requests.Session()
session.post(url=urlLogin, headers=headersForm, data=dates)


responseCountResult = session.post(url=urlCountResult, headers=headersJson, data=json.dumps(paramsCountResult))
result = json.loads(responseCountResult.text)
print(result)
res=jsonpath.jsonpath(result, "$.reportResult.length")
print(res)


# responseCasePlan = session.post(url=urlCasePlen, headers=headersJson, data=json.dumps(paramsCasePlen))
# if responseCasePlan.status_code == 200:
#     print("用例开始执行")

