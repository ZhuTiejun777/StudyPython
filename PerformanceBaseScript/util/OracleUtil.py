import cx_Oracle
import logging
import os

from LogGer import LogGer

LogGer(str(os.path.basename(__file__))[:-3])

class OracleUtil(object):

    def __init__(self, user, password, database):
        cx_Oracle.init_oracle_client(lib_dir="/Users/tiejunzhu/Desktop/profile/instantclient_12_2")
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self._connect = cx_Oracle.connect(self.user, self.password, self.database)

    def insertSql(self, sql):
        cursor = self._connect.cursor()  # 创建游标
        try:
            cursor.execute(sql)
            self._connect.commit()
            #logging.info("插入数据成功:{}".format(sql))
        except Exception as e:
            cursor.rollback()  # 发生错误时回滚
            logging.info("{} 语句执行错误:{}".format(sql, e))

    def selectSql(self, sql):
        cursor = self._connect.cursor()  # 创建游标
        try:
            cursor.execute(sql)  # 执行sql语句
            data = cursor.fetchall()  # 获取一条数据
            # logging.info("{} 查询成功:{}".format(sql, data))  # 打印数据
            return data
        except Exception as e:
            logging.info("{} 语句执行错误:{}".format(sql, e))
            return None

    def getTableNameList(self):
        tableNameList = []
        cursor = self._connect.cursor()
        sqlAll = "select TABLE_NAME from user_tables where TABLE_NAME not like '%$%'"
        cursor.execute(sqlAll)
        tableList = cursor.fetchall()
        for tableName in tableList:
            tableNameList.append(tableName[0])
        return tableNameList

    def selectAllTableCount(self):
        countDict = {}
        cursor = self._connect.cursor()
        tableNameList = self.getTableNameList()
        for tableName in tableNameList:
            sqlCount = "select count(*) from {}".format(tableName)
            print(sqlCount)
            cursor.execute(sqlCount)
            count = cursor.fetchone()
            countDict[tableName] = count[0]
        return countDict