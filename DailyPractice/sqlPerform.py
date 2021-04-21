# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/04/06"

import logging
import os
import random
import pymysql

from LogGer import LogGer


class sqlPerform():

    LogGer(str(os.path.basename(__file__))[:-3])

    def __init__(self, dbConfig):
        self.host = dbConfig['host']
        self.port = dbConfig['port']
        self.user = dbConfig['user']
        self.password = dbConfig['password']
        self.database = dbConfig['database']
        self.charset = dbConfig['charset']
        self._connect = None

    def connect(self):
        self._connect = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, password=self.password,
                                  database=self.database, charset=self.charset)

    def insertSql(self, sqlDict:dict):
        cursor = self._connect.cursor()
        insertSqlStr = self.formatSql(sqlDict)
        logging.info(insertSqlStr)
        try:
            cursor.execute(insertSqlStr)  # 执行sql语句
            self._connect.commit()
            logging.info("执行成功")
        except Exception as e:
            logging.info("执行失败")
            logging.info(e)
            self._connect.rollback()  # 发生错误时回滚

    def insertSqlBak(self, table:str, sqlDict:dict):
        cursor = self._connect.cursor()
        insertSql = ("insert into %s(%s) values(%s)" % (
            table,
            ",".join("{}".format(k) for k in sqlDict.keys()),
            ','.join("'{}'".format(k) for k in sqlDict.values())
            ))
        logging.info(insertSql)
        try:
            cursor.execute(insertSql)
            # 执行sql语句
            self._connect.commit()
            logging.info("执行成功")
        except Exception as e:
            logging.info(e)
            logging.info("执行失败")
            self._connect.rollback()

    def selectSql(self, selectSqlStr:str):
        cursor = self._connect.cursor()
        logging.info(selectSqlStr)
        try:
            cursor.execute(selectSqlStr)  # 执行sql语句
            data = cursor.fetchall()
            print(data)
            logging.info("执行成功")
        except Exception as e:
            logging.info(e)
            logging.info("执行失败")

    def deleteSql(self, deleteSqlStr:str):
        cursor = self._connect.cursor()
        logging.info(deleteSqlStr)
        try:
            cursor.execute(deleteSqlStr)
        except Exception as e:
            logging.info(e)

    def close(self):
        self._connect.close()

    @staticmethod
    def formatSql(sqlDict:dict):
        insertStr = "insert into {} ({}) value ({})"
        columnStr = ""
        valueStr = ""
        number = 0
        for dict in sqlDict:
            number += 1
            if dict == "table":
                continue
            if number == len(sqlDict):
                columnStr = columnStr + dict
                valueStr = valueStr + "'" + str(sqlDict[dict]) + "'"
            else:
                columnStr = columnStr + dict + ","
                valueStr = valueStr + "'" + str(sqlDict[dict]) + "'" + ","
        return insertStr.format(sqlDict.get("table"), columnStr, valueStr)

    @staticmethod
    def randomLengthInt(length:int=10):
        intStr = ""
        if length > 64:
            print("字符长度不可大于64!")
            length = 64
        number = length
        while length:
            if length == number:
                intStr += str(random.randint(1, 9))
            else:
                intStr += str(random.randint(0, 9))
            length -= 1
        return intStr

    @staticmethod
    def randomChinese(count: int = 10):
        import random
        str = ""
        if count < 0 or count > 100:
            print("输入大于0，小于100的数字")
            count = 10
        while count:
            str += chr(random.randint(0x4e00, 0x9fbf))
            count -= 1
        return str

    @staticmethod
    def randomEnglish(count: int = 18):
        import random
        str = ""
        if count < 0 or count > 64:
            print("输入大于0，小于64的数字")
            count = 18
        while count:
            str += chr(random.randint(97, 122))
            count -= 1
        return str

if __name__ == '__main__':
    dbConfig = {
        "host" : "192.168.66.178", "port" : 3306,
        "user" : "loan", "password" : "p2pA!123",
        "database" : "library", "charset" : "utf8"
    }
    #id = sqlPerform.randomLengthInt(18)
    #number = sqlPerform.randomLengthInt(48)

    # insertSqlDict2 = {'table': 'auto_case_config',
    #                  'id': id,
    #                  'needRun': '1',
    #                  'number': number,
    #                  'checkReWrite': 0,
    #                  'cStatus': '1'}

    # insertSqlDictBak = {'id': id,
    #                  'number': 1,
    #                  'inputData': 'test',
    #                  'comment': '1234',
    #                  'needRun': '2',
    #                  'checkReWrite': '4',
    #                  'cStatus': '200'}
    #print(sqlPerform.formatSql(insertSqlDict))
    sqlPerform = sqlPerform(dbConfig)
    sqlPerform.connect()
    number = 50
    while number:
        insertSqlDict = {'table': 'book_info',
                         'name': sqlPerform.randomChinese(random.randint(1, 8)),
                         'author': sqlPerform.randomChinese(random.randint(1, 8)),
                         'publish': sqlPerform.randomChinese(random.randint(1, 8)),
                         'ISBN': '1',
                         'introduction': sqlPerform.randomChinese(random.randint(50, 80)),
                         'language': '200',
                         'price': '11.00',
                         'pub_date': '2021-04-03',
                         'class_id': '1',
                         'number': '1'}
        sqlPerform.insertSql(insertSqlDict)
        number -= 1
    #selectSqlTest = "select * from auto_case_config where number = 'submitCreditApplySuccess-circulation_2'"
    #sqlPerform.selectSql(selectSqlTest)

    #sqlPerform.insertSql(insertSqlDict2)
    #sqlPerform.insertSqlBak("auto_case_tmp", insertSqlDictBak)

    sqlPerform.close()