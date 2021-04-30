# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/04/06"

import datetime
import logging
import os
import random
import pymysql

from LogGer import LogGer

class SqlPerform(object):
    LogGer(str(os.path.basename(__file__))[:-3])

    __sqlPerform = None

    # 返回默认数据库连接
    @classmethod
    def getDb(cls):
        if cls.__sqlPerform == None:
            dbConfig = {
                "host": "192.168.66.178", "port": 3306,
                "user": "loan", "password": "p2pA!123",
                "database": "datafactory", "charset": "utf8"
            }
            cls.__sqlPerform = SqlPerform(dbConfig)
            cls.__sqlPerform.connect()
            return cls.__sqlPerform
        else:
            return cls.__sqlPerform

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

    def insertSqlTest(self, sql):
        cursor = self._connect.cursor()
        logging.info(sql)
        try:
            cursor.execute(sql)  # 执行sql语句
            self._connect.commit()
            # logging.info("执行成功")
        except Exception as e:
            logging.info("执行失败")
            logging.info(e)
            self._connect.rollback()  # 发生错误时回滚

    def insertSql(self, sqlDict: dict, tableName:str):
        cursor = self._connect.cursor()
        insertSqlStr = self.formatSql(sqlDict, tableName)
        logging.info(insertSqlStr)
        try:
            cursor.execute(insertSqlStr)  # 执行sql语句
            self._connect.commit()
            # logging.info("执行成功")
        except Exception as e:
            logging.info("执行失败")
            logging.info(e)
            self._connect.rollback()  # 发生错误时回滚

    def insertSqlBak(self, table: str, sqlDict: dict):
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
            # logging.info("执行成功")
        except Exception as e:
            logging.info(e)
            logging.info("执行失败")
            self._connect.rollback()

    def selectSql(self, selectSqlStr: str):
        cursor = self._connect.cursor()
        logging.info(selectSqlStr)
        try:
            cursor.execute(selectSqlStr)  # 执行sql语句
            data = cursor.fetchall()
            # logging.info("执行成功")
            return data
        except Exception as e:
            logging.info(e)
            logging.info("执行失败")
            return None

    def deleteSql(self, deleteSqlStr: str):
        cursor = self._connect.cursor()
        logging.info(deleteSqlStr)
        try:
            cursor.execute(deleteSqlStr)
        except Exception as e:
            logging.info(e)

    def close(self):
        self._connect.close()

    # 获取排除表字段
    @staticmethod
    def getExcludeTables(storeId: str, dbId: str):
        sql = "select exclude from store_database_configuration where store_id = '{}' and db_id = '{}'".format(storeId,
                                                                                                               dbId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    # 获取备份表字段
    @staticmethod
    def getIncludeTables(storeId: str, dbId: str):
        sql = "select include from store_database_configuration where store_id = '{}' and db_id = '{}'".format(storeId,
                                                                                                               dbId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    # 获取排除表字段
    @staticmethod
    def getStoreIDByRecordId(recordId: str):
        sql = "select store_id from datafactory.store_record_info where id = '{}'".format(recordId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    # 根据storeId查询数据库配置
    @staticmethod
    def getDbidByStoreId(storeId: str):
        sql = "select db_id from store_database_configuration where store_id = '{}'".format(storeId)
        tupleDbId = SqlPerform.getDb().selectSql(sql)
        listDbId = []
        for dbId in tupleDbId:
            listDbId.append(dbId[0])
        return listDbId

    # 查询数据库名称配置
    @staticmethod
    def getDbNameByDbId(dbId: str):
        sql = "select db_name from database_connect_info where id = '{}'".format(dbId)
        listLibrary = SqlPerform.getDb().selectSql(sql)[0][0].split(";")
        logging.info("读取数据库为:{}".format(listLibrary))
        return listLibrary

    sqlPerformTarget = None

    # 返回配置中的服务器连接
    @staticmethod
    def getTargetDb(dbId, dbName):
        sql = "select db_host,db_port,db_user,db_password from database_connect_info where id = '{}'".format(
            dbId)
        if SqlPerform.sqlPerformTarget is None:
            db_host, db_port, db_user, db_password = SqlPerform.getDb().selectSql(sql)[0]
            dbConfig = {
                "host": db_host, "port": db_port,
                "user": db_user, "password": db_password,
                "database": dbName, "charset": "utf8"
            }
            SqlPerform.sqlPerformTarget = SqlPerform(dbConfig)
            SqlPerform.sqlPerformTarget.connect()
            return SqlPerform.sqlPerformTarget
        else:
            return SqlPerform.sqlPerformTarget

    @staticmethod
    def insertSqlTargetDb(dbId:str, dbName:str, insertSqlStr:str):
        SqlPerform.getTargetDb(dbId, dbName).insertSqlTest(insertSqlStr)


    @staticmethod
    def performTargetIsNone():
        SqlPerform.sqlPerformTarget = None

    # 获取所有表
    @staticmethod
    def getAllTable(dbId: str, dbName: str):
        sql = "select table_name from information_schema.tables where table_schema='{}'".format(dbName)
        # return SqlPerform.getDb().selectSql(sql)
        tupleTable = SqlPerform.getTargetDb(dbId, dbName).selectSql(sql)
        listTable = []
        for tableName in tupleTable:
            listTable.append(tableName[0])
        logging.info("数据库表为{}".format(listTable))
        return listTable

    # 获取表所有数据条数
    @staticmethod
    def getTableCount(dbId: str, dbName: str, table: str):
        # logging.info("查询所有表名:{}".format(table))
        sql = "select count(*) from {}".format(table)
        # return SqlPerform.getDb().selectSql(sql)[0][0]
        count = SqlPerform.getTargetDb(dbId, dbName).selectSql(sql)[0][0]
        logging.info("{}表数据总数{}".format(table, count))
        return int(count)

    @staticmethod
    def formatSql(sqlDict:dict, table:str):
        insertStr = "insert into {} ({}) value ({})"
        columnStr = ""
        valueStr = ""
        number = 0
        for dict in sqlDict:
            number += 1
            if sqlDict[dict] == None:
                continue
            if number == len(sqlDict):
                columnStr = columnStr + dict
                valueStr = valueStr + "'" + str(sqlDict[dict]) + "'"
            else:
                columnStr = columnStr + dict + ","
                valueStr = valueStr + "'" + str(sqlDict[dict]) + "'" + ","
        return insertStr.format(table, columnStr, valueStr)

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

    @staticmethod
    def getDate():
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    @staticmethod
    def selectNameTypeDefault(dbId, dbName, tableName):
        sql = "select column_name,column_type,column_default from information_schema.COLUMNS where LOWER(table_name) = '{}'".format(tableName)
        result = SqlPerform.getTargetDb(dbId, dbName).selectSql(sql)
        dictTablle = {}
        for tuples in result:
            columnName, columnType, columnDefault = tuples
            columnTypeRes = None
            columnTypeNum = None
            columnTypeDou = None
            if "," in columnType:
                columnTypeRes = columnType.split("(")[0]
                columnTypeNum = int(columnType.split("(")[1].split(",")[0])
                columnTypeDou = int((columnType.split(",")[1].split(")")[0]))
            else:
                if "(" in columnType:
                    columnTypeRes = columnType.split("(")[0]
                    columnTypeNum = int(columnType.split("(")[1].split(")")[0])
                else:
                    columnTypeRes = columnType
            #print(columnType, columnTypeRes, columnTypeNum, columnTypeDou)
            if columnDefault == None:
                if columnTypeRes == "text":
                    dictTablle[columnName] = SqlPerform.randomChinese(30)
                elif columnTypeRes == "varchar" or columnTypeRes == "char":
                    dictTablle[columnName] = SqlPerform.randomEnglish(random.randint(1, columnTypeNum))
                elif columnTypeRes == "bigint":  # 9223372036854775807
                    if columnTypeNum >= 18:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, 18))
                    else:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, columnTypeNum))
                elif columnTypeRes == "int":  # 2147483647
                    if columnTypeNum >= 10:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, 10))
                    else:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, columnTypeNum))
                elif columnTypeRes == "decimal" or columnTypeRes == "float" or columnTypeRes == "double":
                    dictTablle[columnName] = SqlPerform.randomLengthInt(
                        random.randint(1, columnTypeNum - columnTypeDou))
                elif columnTypeRes == "date" or columnTypeRes == "time" or columnTypeRes == "datetime":
                    dictTablle[columnName] = SqlPerform.getDate()
            else:
                dictTablle[columnName] = None
        sql = SqlPerform.formatSql(dictTablle, tableName)
        return sql




def test(DbId:str, DbName:str, cycles:int):
    tableList = SqlPerform.getAllTable(DbId, DbName)
    while cycles:
        sql = SqlPerform.selectNameTypeDefault(DbId, DbName, tableList[random.randint(0, len(tableList)-1)])
        SqlPerform.insertSqlTargetDb(DbId, DbName, sql)
        cycles -= 1
    SqlPerform.performTargetIsNone()

test("221658682067255296", "library", 10)