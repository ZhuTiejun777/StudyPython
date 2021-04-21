# -*- coding: UTF-8 -*-
__Author__ = "zhutj"
__Date__ = "2021/04/08"

import logging
import os
import re
import time
from logging import handlers

import paramiko
import pymysql


class LogGer(object):
    def __init__(self, name):
        os.makedirs("./log") if not os.path.exists("./log") else None  # 创建日志文件文件夹
        get_logger_a = logging.getLogger()
        get_logger_a.setLevel(logging.INFO)  # 设置默认级别
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d]: %(message)s')
        log_file_path = './log/{}_{}.log'.format(name, time.strftime('%Y%m%d'))
        rotating_handler = handlers.RotatingFileHandler(
            log_file_path, maxBytes=20 * 1024 * 1024, backupCount=10, encoding='utf-8')
        rotating_handler.setFormatter(formatter)
        get_logger_a.addHandler(rotating_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        get_logger_a.addHandler(stream_handler)
        # 过滤级别：控制台输出INFO和WARNING级别，文件只记录WARNING级别
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno < logging.INFO  # 设置过滤等级
        warn_filter = logging.Filter()
        warn_filter.filter = lambda record: record.levelno >= logging.INFO
        # stream_handler.addFilter(info_filter)
        rotating_handler.addFilter(warn_filter)


LogGer(str(os.path.basename(__file__))[:-3])


class SSHConnection(object):
    __mycon = None

    # 返回默认服务器连接
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
        # logging.info(command)
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        res, err = stdout.readlines(), stderr.readlines()
        # result = err if err else "正常执行"
        # logging.info(result)
        return res, err

    def __del__(self):
        self.close()

    # 获取指定文件行数
    @staticmethod
    def getDirCount(recordId, storeId, dbId, dbName, tableName):
        strShell = "wc -l /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/" + tableName
        # getPid = "ps -ef|grep tomcat|grep -v grep|awk '{print $2}'"
        res, err = SSHConnection.getSSHConn().run_cmd(strShell)
        count = res[0].split(" ")[0]
        logging.info("{}备份数据总数为{}".format(tableName, count))
        return int(count)

    # 获取指定目录下所有文件总数
    @staticmethod
    def getDirsCount(recordId, storeId, dbId, dbName):
        getDirs = "cd /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/; ls -l| grep '^-'| wc -l"
        res, err = SSHConnection.getSSHConn().run_cmd(getDirs)
        count = res[0].split(" ")[0]
        return int(count)

    # 获取指定目录下所有文件名称
    @staticmethod
    def getDirsName(recordId, storeId, dbId, dbName):
        getDirsName = "cd /home/store/" + recordId + "/" + storeId + "/" + dbId + "/" + dbName + "/; ls -l |grep -v total|awk '{print $9}'"
        res, err = SSHConnection.getSSHConn().run_cmd(getDirsName)
        dirsName = []
        for dirName in res:
            dirsName.append(dirName.split("\n")[0])
        logging.info("备份数据库:{}".format(dbName))
        return dirsName


class SqlPerform(object):
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

    def insertSql(self, sqlDict: dict):
        cursor = self._connect.cursor()
        insertSqlStr = self.formatSql(sqlDict)
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


def contrastData(recordId):
    # agree = 0
    agreeList = []
    # unagree = 0
    unAgreeList = []
    # 根据recordId获取recordId
    storeId = SqlPerform.getStoreIDByRecordId(recordId)
    # 获取所有数据库dbId
    for dbId in SqlPerform.getDbidByStoreId(storeId):
        # 根据dbId获取dbName
        for dbName in SqlPerform.getDbNameByDbId(dbId):
            # print(dbName)
            # 判断备份表是否有数据
            if SqlPerform.getIncludeTables(storeId, dbId).strip() == "" or SqlPerform.getIncludeTables(storeId,
                                                                                                       dbId) is None:
                # 判断排除表是否有数据
                if SqlPerform.getExcludeTables(storeId, dbId).strip() == "" or SqlPerform.getExcludeTables(storeId,
                                                                                                           dbId) is None:
                    logging.info("{}:备份表没数据，排除表没数据".format(dbName))
                    # 获取指定数据库所有表
                    listTable = SqlPerform.getAllTable(dbId, dbName)
                    listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)  # threeLevel --> dbId
                    # 备份数据判断
                    agreeTempList, unAgreeTempList = contrastTable(storeId, recordId, dbId, dbName, listTable,
                                                                   listDirName)
                    agreeList.append(agreeTempList)
                    unAgreeList.append(unAgreeTempList)
                    # 重置数据库连接连接
                    SqlPerform.performTargetIsNone()
                else:
                    logging.info("{}:备份表没数据，排除表有数据".format(dbName))
                    # 获取指定数据库所有表
                    reStrs = SqlPerform.getExcludeTables(storeId, dbId).strip()
                    listTable = getExcludeListRe(reStrs, SqlPerform.getAllTable(dbId, dbName))
                    listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)  # threeLevel --> dbId
                    # 备份数据判断
                    agreeTempList, unAgreeTempList = contrastTable(storeId, recordId, dbId, dbName, listTable,
                                                                   listDirName)
                    agreeList.append(agreeTempList)
                    unAgreeList.append(unAgreeTempList)
                    # 重置数据库连接连接
                    SqlPerform.performTargetIsNone()
            else:
                # 判断排除表是否有数据
                if SqlPerform.getExcludeTables(storeId, dbId).strip() == "" or SqlPerform.getExcludeTables(storeId,
                                                                                                           dbId) is None:
                    logging.info("{}:备份表有数据，排除表没有数据".format(dbName))
                    # 获取备份表字段值
                    reStrs = SqlPerform.getIncludeTables(storeId, dbId).strip()
                    # 获取指定数据库所有表
                    listTable = getIncludeListRe(reStrs, SqlPerform.getAllTable(dbId, dbName))
                    # 获取服务器所有备份数据名称
                    listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)  # threeLevel --> dbId
                    # 备份数据判断
                    agreeTempList, unAgreeTempList = contrastTable(storeId, recordId, dbId, dbName, listTable,
                                                                   listDirName)
                    agreeList.append(agreeTempList)
                    unAgreeList.append(unAgreeTempList)
                    # 重置数据库连接连接
                    SqlPerform.performTargetIsNone()
                else:
                    logging.info("{}:备份表没有数据，排除表没有数据".format(dbName))
                    # 获取备份表字段值
                    reIncludeStrs = SqlPerform.getIncludeTables(storeId, dbId).strip()
                    # 获取指定数据库所有表
                    listIncludeTable = getIncludeListRe(reIncludeStrs, SqlPerform.getAllTable(dbId, dbName))
                    # 获取排除表字段值
                    reExcludeStrs = SqlPerform.getExcludeTables(storeId, dbId).strip()
                    # 匹配备份表后在匹配排除表
                    listTable = getExcludeListRe(reExcludeStrs, listIncludeTable)
                    # 获取服务器所有备份数据名称
                    listDirName = SSHConnection.getDirsName(recordId, storeId, dbId, dbName)  # threeLevel --> dbId
                    # 备份数据判断
                    agreeTempList, unAgreeTempList = contrastTable(storeId, recordId, dbId, dbName, listTable,
                                                                   listDirName)
                    agreeList.append(agreeTempList)
                    unAgreeList.append(unAgreeTempList)
                    # 重置数据库连接连接
                    SqlPerform.performTargetIsNone()
    # logging.info("{}表数据一致".format(agreeList))
    logging.error("{}表数据不一致".format(unAgreeList))


# 备份数据判断
def contrastTable(storeId, recordId, dbId, dbName, listTable, listDirName):
    agreeList = []
    unagreeList = []
    diffList = [y for y in (listTable + listDirName) if
                y not in [x for x in listTable if x in listDirName]]
    # 判断表数量和备份数量是否一致
    if SSHConnection.getDirsCount(recordId, storeId, dbId, dbName) == len(listTable):  # threeLevel --> dbId
        # 判断表名称与备份名称是否一致
        if len(diffList) == 0:
            # 遍历所有表获取表名称
            for tableName in listTable:
                # 根据表名获取表数据行数
                tableCount = SqlPerform.getTableCount(dbId, dbName, tableName)
                # 根据表名获取备份文件行数
                dirCount = SSHConnection.getDirCount(recordId, storeId, dbId, dbName, tableName)  # threeLevel --> dbId
                if tableCount == dirCount:
                    logging.info("{}数据与备份数据一致".format(tableName))
                    logging.info("-" * 50)
                    agreeList.append(tableName)
                else:
                    logging.error("{}数据与备份数据不一致".format(tableName))
                    logging.info("-" * 50)
                    unagreeList.append(tableName)
        else:
            logging.error("表名称与备份文件不一致,差别表:{}".format(diffList))
    # 数量不一致退出本次循环
    else:
        # logging.error("表数量与备份数量不一致,备份表:{},备份数据:{}".format(listTable, listDirName))
        logging.error("表数量与备份数量不一致,差别表:{}".format(diffList))
    return agreeList, unagreeList


# 根据正则匹配表名返回排除表
def getExcludeListRe(reStrs: str, tableList: list):
    reListTable = []
    for reStr in reStrs.split(";"):
        for table in tableList:
            # TODO 匹配方式与项目不符
            pattern = re.compile(reStr)
            result = pattern.findall(table)
            # logging.info("正则规则:{},表名:{},匹配后的结果:{}".format(reStr, table, result))
            if len(result) == 0 or result[0] != table:
                reListTable.append(table)
    logging.info("匹配后的表{}".format(reListTable))
    return reListTable


# 根据正则匹配表名返回备份表
def getIncludeListRe(reStrs: str, tableList: list):
    reListTable = []
    for reStr in reStrs.split(";"):
        for table in tableList:
            # TODO 匹配方式与项目不符
            pattern = re.compile(reStr)
            result = pattern.findall(table)
            if len(result) != 0:
                reListTable.append(table)
    logging.info("匹配后的表{}".format(reListTable))
    return reListTable


if __name__ == '__main__':
    # pathStr = "/Users/tiejunzhu/Desktop/220955214667055104/220953969797627904/220944994133868544/datafactory"

    # print(listDir(pathStr))

    # count = len(open(pathStr,'rb').readlines())
    # print(count)
    # sql = "select count(*) from {}".format("store_analyse_info")
    # dbConfig = {
    #     "host": "192.168.66.178", "port": 3306,
    #     "user": "loan", "password": "p2pA!123",
    #     "database": "datafactory", "charset": "utf8"
    # }
    # sqlPerform = SqlPerform(dbConfig).connect()
    # print(sqlPerform.selectSql(sql))

    # print(SqlPerform.tableCount("store_analyse_info"))
    # print(SqlPerform.getAllTable())

    # dictCheck = {
    #     "projectId": "224493763144187904",
    #     "storeId": "224493723487043584",
    #     "recordId": "221658682067255296",
    #     "dbId": "221658428181839872",
    # }
    # projectId, storeId, recordId, dbName, tableName
    # print(SSHConnection.getDirsCount())
    # list = SSHConnection.getDirsName(dictCheck.get("projectId"),
    #                                  dictCheck.get("storeId"),
    #                                  dictCheck.get("recordId"),
    #                                  dictCheck.get("dbName"),)
    # print(list)

    # print(SqlPerform.getTargetDb(dictCheck.get("dbId")))

    # sql = "select db_host,db_port,db_user,db_password,db_name from datafactory.database_connect_info where id = '{}'".format(dictCheck.get("dbId"))
    # db_host, db_port, db_user, db_password, db_name = SqlPerform.getDb().selectSql(sql)[0]
    # print(db_host)

    # tupleTable = SqlPerform.getAllTable(dictCheck.get("dbId"))
    # print(tupleTable)
    # list = []
    # for i in tupleTable:
    #    list.append(i[0])
    # print(list)

    # print(len(SqlPerform.getAllTable("223841724437364736", "library")))
    # 224466023431012352  #225644756347125760
    contrastData("225981383263125504")
    # contrastData("225642346576871424", "224466023431012352", "223826490662322176")
    # tableCount = SqlPerform.getTableCount("223841724437364736", "admin")
    # dirCount = SSHConnection.getDirCount("225547359029821440", "224169917165862912", "223841724437364736", "library", "admin")
    # print(tableCount)
    # print(dirCount)
    # print(type(tableCount))
    # print(type(tableCount))
    # print(SqlPerform.getStoreIDByRecordId("225981393069408256"))
