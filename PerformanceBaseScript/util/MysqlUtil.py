# -*- coding: UTF-8 -*-
__Author__ = "zhutiejun777"
__Date__ = "2021/03/01"
import logging
import os
import pymysql

from LogGer import LogGer

LogGer(str(os.path.basename(__file__))[:-3])


class MysqlUtil(object):
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
        try:
            cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            logging.info(e)
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
