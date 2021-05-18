import json
import os

import pymongo


class ConnMongoDB:

    def __init__(self):
        myClient = pymongo.MongoClient(host="192.168.66.172", port=28017)
        myDB = myClient.admin
        myDB.authenticate("root", "D1w119hsJry0")
        myTables = myClient.credit_report
        self.collection = myTables.target_field

    # 根据reportCode查询content
    def selectContent(self, reportCode):
        result = self.collection.find_one({"report_code": reportCode})
        return result["content"]

    def getCount(self):
        count = 0
        sets = self.collection.find({}, {"_id": 1})
        for setDict in sets:
            count += 1
        return count

    # 读取content数据
    @staticmethod
    def readContentJson():
        fieldsPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "BaseData/content.json")
        with open(fieldsPath, mode='r', encoding="UTF-8") as f:
            contentJson = json.load(f)
            f.close()
        return contentJson

    # 读取reportCode文件，返回list
    @staticmethod
    def readResultCSV():
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "BaseData/result.csv")
        with open(path, mode='r', encoding="UTF-8") as f:
            context = f.readlines()
            f.close()
        reportCodeList = []
        for line in context:
            reportCodeList.append(line.strip())
        return reportCodeList

    # 根据reportCode读取response返回fieldsJson
    @staticmethod
    def resultDict(reportCode):
        reportCodePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "responseJson/" + reportCode + ".json")
        with open(reportCodePath, mode='r', encoding="UTF-8") as f:
            reportCodeJsonList = json.load(f)
            f.close()
        resultDict = {}
        resultDict["reportCode"] = reportCode
        for reportCodeJson in reportCodeJsonList:
            resultDict[reportCodeJson["key"]] = reportCodeJson["val"]
        return resultDict

    # 获取基础fieldsJson
    @staticmethod
    def readFieldsJson():
        fieldsPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "BaseData/fields.json")
        with open(fieldsPath, mode='r', encoding="UTF-8") as f:
            fieldsJson = json.load(f)
            f.close()
        return fieldsJson

    # 对比基础fieldsJson和responseJson区别
    @staticmethod
    def resultCompare(fieldsJson, resultDict):
        for key in fieldsJson:
            if fieldsJson[key] == resultDict[key]:
                del resultDict[key]
            else:
                print("实时返回接口 {} 数据指标 {}:{} 存在差异".format(resultDict["reportCode"], key, fieldsJson[key]))
        if len(resultDict) != 1:
            print("{}剩余数据:{}".format(resultDict["reportCode"], resultDict))


if __name__ == '__main__':

    # 读取reportCodeList
    reportCodeList = ConnMongoDB.readResultCSV()

    # 读取contentJson
    contentJson = ConnMongoDB.readContentJson()

    # 读取fieldsJson
    fieldsJson = ConnMongoDB.readFieldsJson()

    #errList = []

    # 对比mongo中数据
    conn = ConnMongoDB()
    for reportCode in reportCodeList:
        resultDict = conn.selectContent(reportCode)
        # 判断content长度是否相等
        if len(resultDict) != 2086:
            print("差异数据量 " + reportCode, len(conn.selectContent(reportCode)))
            #errList.append(reportCode)
        # 判读content数据是否相等
        if contentJson != resultDict:
            print("mongo中 {} 数据结果不正确".format(reportCode))
            #errList.append(reportCode)
        # 接口实时返回值对比
        responseFieldsJson = conn.resultDict(reportCode)
        conn.resultCompare(fieldsJson, responseFieldsJson)

    # mongo中总数据量
    print("数据总量" + str(conn.getCount()))  # 24458
