# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/04/14"

import datetime
import random
import re

import paramiko
import pymysql


class SSHConnection(object):
    __mycon = None

    @classmethod
    def getSSHConn(cls):
        if cls.__mycon == None:
            host = {"host": "192.168.66.179", "port": 22, "username": "root", "password": "Yrjk%test123"}
            cls.__mycon = SSHConnection(host)
            cls.__mycon.connect()
            return cls.__mycon
        else:
            return cls.__mycon

    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        res, err = stdout.readlines(), stderr.readlines()
        return res, err

    def __del__(self):
        self.close()

    @staticmethod
    def getDirCount(recordId, storeId, dbId, dbName, tableName):
        strShell = "wc -l /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/" + tableName
        res, err = SSHConnection.getSSHConn().run_cmd(strShell)
        count = res[0].split(" ")[0]
        return int(count)

    @staticmethod
    def getDirsCount(recordId, storeId, dbId, dbName):
        getDirs = "cd /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/; ls -l| grep '^-'| wc -l"
        res, err = SSHConnection.getSSHConn().run_cmd(getDirs)
        count = res[0].split(" ")[0]
        return int(count)

    @staticmethod
    def getDirsName(recordId, storeId, dbId, dbName):
        getDirsName = "cd /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/; ls -l |grep -v total|awk '{print $9}'"
        res, err = SSHConnection.getSSHConn().run_cmd(getDirsName)
        dirsName = []
        for dirName in res:
            dirsName.append(dirName.split("\n")[0])
        return dirsName


class SqlPerform(object):
    __sqlPerform = None

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

    def insertSql(self, sqlDict: dict, tableName: str):
        cursor = self._connect.cursor()
        insertSqlStr = self.formatSql(sqlDict, tableName)
        try:
            cursor.execute(insertSqlStr)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()

    def insertSqlTest(self, sql):
        cursor = self._connect.cursor()
        try:
            cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            print(e)
            self._connect.rollback()

    def insertSqlBak(self, table: str, sqlDict: dict):
        cursor = self._connect.cursor()
        insertSql = ("insert into %s(%s) values(%s)" % (
            table,
            ",".join("{}".format(k) for k in sqlDict.keys()),
            ','.join("'{}'".format(k) for k in sqlDict.values())
        ))
        try:
            cursor.execute(insertSql)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()

    def selectSql(self, selectSqlStr: str):
        cursor = self._connect.cursor()
        try:
            cursor.execute(selectSqlStr)
            data = cursor.fetchall()
            return data
        except Exception as e:
            return None

    def deleteSql(self, deleteSqlStr: str):
        cursor = self._connect.cursor()
        try:
            cursor.execute(deleteSqlStr)
        except Exception as e:
            return None

    def close(self):
        self._connect.close()

    @staticmethod
    def getExcludeTables(storeId: str, dbId: str):
        sql = "select exclude from store_database_configuration where store_id = '{}' and db_id = '{}'".format(storeId,
                                                                                                               dbId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    @staticmethod
    def getIncludeTables(storeId: str, dbId: str):
        sql = "select include from store_database_configuration where store_id = '{}' and db_id = '{}'".format(storeId,
                                                                                                               dbId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    @staticmethod
    def getStoreIDByRecordId(recordId: str):
        sql = "select store_id from datafactory.store_record_info where id = '{}'".format(recordId)
        return SqlPerform.getDb().selectSql(sql)[0][0]

    @staticmethod
    def getDbidByStoreId(storeId: str):
        sql = "select db_id from store_database_configuration where store_id = '{}'".format(storeId)
        tupleDbId = SqlPerform.getDb().selectSql(sql)
        listDbId = []
        for dbId in tupleDbId:
            listDbId.append(dbId[0])
        return listDbId

    @staticmethod
    def getDbNameByDbId(dbId: str):
        sql = "select db_name from database_connect_info where id = '{}'".format(dbId)
        listLibrary = SqlPerform.getDb().selectSql(sql)[0][0].split(";")
        return listLibrary

    sqlPerformTarget = None

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
    def insertSqlTargetDb(dbId: str, dbName: str, insertSqlStr: str):
        print(insertSqlStr)
        SqlPerform.getTargetDb(dbId, dbName).insertSqlTest(insertSqlStr)

    @staticmethod
    def performTargetIsNone():
        SqlPerform.sqlPerformTarget = None

    @staticmethod
    def formatSql(sqlDict: dict, table: str):
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
    def getAllTable(dbId: str, dbName: str):
        sql = "select table_name from information_schema.tables where table_schema='{}'".format(dbName)
        tupleTable = SqlPerform.getTargetDb(dbId, dbName).selectSql(sql)
        listTable = []
        for tableName in tupleTable:
            listTable.append(tableName[0])
        return listTable

    @staticmethod
    def getTableCount(dbId: str, dbName: str, table: str):
        sql = "select count(*) from {}".format(table)
        count = SqlPerform.getTargetDb(dbId, dbName).selectSql(sql)[0][0]
        return int(count)

    @staticmethod
    def randomLengthInt(length: int = 10):
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
        sql = "select column_name,column_type,column_default from information_schema.COLUMNS where LOWER(table_name) = '{}'".format(
            tableName)
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
            if columnDefault == None:
                if columnTypeRes == "text":
                    dictTablle[columnName] = SqlPerform.randomChinese(random.randint(10, 30))
                elif columnTypeRes == "varchar" or columnTypeRes == "char":
                    dictTablle[columnName] = SqlPerform.randomEnglish(random.randint(1, columnTypeNum))
                elif columnTypeRes == "bigint":  # 9223372036854775807
                    if columnTypeNum >= 18:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, 18))
                    else:
                        dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, columnTypeNum))
                elif columnTypeRes == "int":  # 2147483647
                    if columnTypeNum >= 10:
                        # dictTablle[columnName] = SqlPerform.randomLengthInt(random.randint(1, 9))
                        dictTablle[columnName] = random.randint(1000000000, 2147483647)
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

    @staticmethod
    def randomInsertSqlByStoreId(storeId: str, cycles: int):
        dbIdList = SqlPerform.getDbidByStoreId(storeId)
        for dbId in dbIdList:
            dbNameList = SqlPerform.getDbNameByDbId(dbId)
            while cycles:
                dbName = dbNameList[random.randint(0, len(dbNameList) - 1)]
                tableList = SqlPerform.getAllTable(dbId, dbName)
                sql = SqlPerform.selectNameTypeDefault(dbId, dbName, tableList[random.randint(0, len(tableList) - 1)])
                SqlPerform.insertSqlTargetDb(dbId, dbName, sql)
                cycles -= 1
            SqlPerform.performTargetIsNone()


class CheckDb():

    @staticmethod
    def contrastData(recordId: str):
        agreeList = []
        unAgreeList = []
        storeId = SqlPerform.getStoreIDByRecordId(recordId)
        for dbId in SqlPerform.getDbidByStoreId(storeId):
            for dbName in SqlPerform.getDbNameByDbId(dbId):
                if SqlPerform.getIncludeTables(storeId, dbId).strip() == "" or SqlPerform.getIncludeTables(storeId,
                                                                                                           dbId) is None:
                    if SqlPerform.getExcludeTables(storeId, dbId).strip() == "" or SqlPerform.getExcludeTables(storeId,
                                                                                                               dbId) is None:
                        listTable = SqlPerform.getAllTable(dbId, dbName)
                        listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)
                        agreeTempList, unAgreeTempList = CheckDb.contrastTable(storeId, recordId, dbId, dbName,
                                                                               listTable,
                                                                               listDirName)
                        agreeList.extend(agreeTempList)
                        unAgreeList.extend(unAgreeTempList)
                    else:
                        reStrs = SqlPerform.getExcludeTables(storeId, dbId).strip()
                        listTable = CheckDb.getExcludeListRe(reStrs, SqlPerform.getAllTable(dbId, dbName))
                        listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)
                        agreeTempList, unAgreeTempList = CheckDb.contrastTable(storeId, recordId, dbId, dbName,
                                                                               listTable,
                                                                               listDirName)
                        agreeList.extend(agreeTempList)
                        unAgreeList.extend(unAgreeTempList)
                else:
                    if SqlPerform.getExcludeTables(storeId, dbId).strip() == "" or SqlPerform.getExcludeTables(storeId,
                                                                                                               dbId) is None:
                        reStrs = SqlPerform.getIncludeTables(storeId, dbId).strip()
                        listTable = CheckDb.getIncludeListRe(reStrs, SqlPerform.getAllTable(dbId, dbName))
                        listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)
                        agreeTempList, unAgreeTempList = CheckDb.contrastTable(storeId, recordId, dbId, dbName,
                                                                               listTable,
                                                                               listDirName)
                        agreeList.extend(agreeTempList)
                        unAgreeList.extend(unAgreeTempList)
                    else:
                        reIncludeStrs = SqlPerform.getIncludeTables(storeId, dbId).strip()
                        listIncludeTable = CheckDb.getIncludeListRe(reIncludeStrs, SqlPerform.getAllTable(dbId, dbName))
                        reExcludeStrs = SqlPerform.getExcludeTables(storeId, dbId).strip()
                        listTable = CheckDb.getExcludeListRe(reExcludeStrs, listIncludeTable)
                        listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)
                        agreeTempList, unAgreeTempList = CheckDb.contrastTable(storeId, recordId, dbId, dbName,
                                                                               listTable,
                                                                               listDirName)
                        agreeList.extend(agreeTempList)
                        unAgreeList.extend(unAgreeTempList)
                SqlPerform.performTargetIsNone()
        if len(unAgreeList) == 0:
            # return True
            return "备份数据与表数据一致"
        else:
            # return False
            return "{}表数据存在差异".format(unAgreeList)

    @staticmethod
    def contrastTable(storeId: str, recordId: str, dbId: str, dbName: str, listTable: list, listDirName: list):
        agreeList = []
        unagreeList = []
        diffList = [y for y in (listTable + listDirName) if
                    y not in [x for x in listTable if x in listDirName]]
        if SSHConnection.getDirsCount(recordId, storeId, dbId, dbName) == len(listTable):
            if len(diffList) == 0:
                for tableName in listTable:
                    tableCount = SqlPerform.getTableCount(dbId, dbName, tableName)
                    dirCount = SSHConnection.getDirCount(recordId, storeId, dbId, dbName,
                                                         tableName)
                    if tableCount == dirCount:
                        agreeList.append(tableName)
                    else:
                        unagreeList.append(tableName)
        return agreeList, unagreeList

    @staticmethod
    def getExcludeListRe(reStrs: str, tableList: list):
        reListTable = []
        for reStr in reStrs.split(";"):
            for table in tableList:
                pattern = re.compile(reStr)
                result = pattern.findall(table)
                if len(result) != 0:
                    reListTable.append(table)
        reListTable = list(set(reListTable))
        for listTemp in reListTable:
            tableList.remove(listTemp)
        return tableList

    @staticmethod
    def getIncludeListRe(reStrs: str, tableList: list):
        reListTable = []
        for reStr in reStrs.split(";"):
            for table in tableList:
                pattern = re.compile(reStr)
                result = pattern.findall(table)
                if len(result) != 0:
                    reListTable.append(table)
        return reListTable


def checkDb(recordId: str):
    """
    校验备份文件与数据库文件差别
    """
    return CheckDb.contrastData(recordId)


def randomInsertSql(storeId: str, cycles: int):
    """
    随机插入cycles条数据
    """
    SqlPerform.randomInsertSqlByStoreId(storeId, cycles)
