import pymysql


class SelectDB(object):
    __sqlPerform = None

    @classmethod
    def getDb(cls):
        if cls.__sqlPerform == None:
            dbConfig = {
                "host": "192.168.66.178", "port": 3306,
                "user": "loan", "password": "p2pA!123",
                "database": "datafactory", "charset": "utf8"
            }
            cls.__sqlPerform = SelectDB(dbConfig)
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



