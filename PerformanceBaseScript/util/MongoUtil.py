# -*- coding: UTF-8 -*-
__Author__ = "zhutiejun777"
__Date__ = "2021/03/01"

import pymongo as pymongo


class MongoUtil(object):

    def __init__(self, host, port):
        self.myClient = pymongo.MongoClient(host=host, port=port)
        self.myDB = self.myClient.admin

    def connect(self, username, password, DbName, TableName):
        self.myDB.authenticate(username, password)
        self.myTables = self.myClient[DbName]
        self.collection = self.myTables[TableName]

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
