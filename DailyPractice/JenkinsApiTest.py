# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/05/10"

import json
import time

import jsonpath
import requests

urlRun = "http://192.168.66.178:8080/AutoWeb/runPlanForJenkins"
urlResult = "http://192.168.66.178:8080/AutoWeb/queryRunResult"

headersJson = {
    "Content-Type": "application/json;charset=UTF-8"
}

paramsRun = {
    "planNames": ["test"],
    "productName": "datafactory",
    "versionName": "truck",
    "configName": "loaclTest",
    "notice": False
}

responseRun = requests.post(url=urlRun, headers=headersJson, data=json.dumps(paramsRun))
responseRunText = json.loads(responseRun.text)
print(responseRunText)

runId = ""
if jsonpath.jsonpath(responseRunText, "$.success"):
    runId = jsonpath.jsonpath(responseRunText, "$.runId")[0]
    print(runId)
else:
    print("请求失败")


def result(runId):
    paramsResult = {
        "runId": runId
    }
    responseResult = requests.post(url=urlResult, headers=headersJson, data=json.dumps(paramsResult))
    responseResultText = json.loads(responseResult.text)
    return jsonpath.jsonpath(responseResultText, "$.runResult")[0]


boolResult = True
while boolResult:
    time.sleep(1)
    if result(runId) == "pass":
        print("运行完成")
        boolResult = False
    print(result(runId))
