import json
import os
import re
import time
import unittest
import cx_Oracle as cx

from util.OracleUtil import OracleUtil
from util.SSHUtil import SSHUtil
from util.Tools import randomEnglishInt


class TestDir(unittest.TestCase):

    def test01(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test")
        f = open(file=path, mode="r", encoding="utf-8")
        line = f.readline()
        while line:
            line = line.strip()
            reLine = re.sub(" +", "\t", line)
            str, annotation = reLine.split("\t")
            # self.interval_type = parameters["interval_type"]  # 还款间隔
            # print("self." + str + ' = parameters["' + str + '"]  # ' + annotation)
            print(str + ' = "' + str + '"  # ' + annotation)
            line = f.readline()
        f.close()

    def test(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test")
        f = open(file=path, mode="r", encoding="utf-8")
        line = f.readline()
        strResult = ""
        while line:
            line = line.strip()
            reLine = re.sub(" +", "\t", line)
            str = reLine.split("\t")[0]
            # self.interval_type = parameters["interval_type"]  # 还款间隔
            # print("self." + str + ' = parameters["' + str + '"]  # ' + annotation)
            line = f.readline()
            strResult += str + ", "
        f.close()
        print(strResult)

    def test02(self):
        date = "20210519"
        root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('test')[0], "result", date)
        os.makedirs(root_path) if not os.path.exists(root_path) else print("{}文件已创建".format(root_path))

        customer_path = os.path.join(root_path, "customer_" + date + ".txt")
        customer_file = open(file=customer_path, mode="w", encoding="utf-8")

        rows = 10
        customer_file.write("dataRowCount|+|" + str(rows) + "\n")
        while rows:
            customer_no = "customer_no"
            cert_type = "cert_type"
            cert_no = "cert_no"
            name = "name"
            strLine = self.strJoin(customer_no, cert_type, cert_no, name)
            print(strLine)
            customer_file.write(strLine)
            rows -= 1
        customer_file.close()

    @staticmethod
    def strJoin(*parameters):
        strResult = ""
        lenParameters = len(parameters)
        for parameter in parameters:
            strResult += parameter
            lenParameters -= 1
            if lenParameters != 0:
                strResult += "|+|"
            else:
                strResult += "\n"
        return strResult

    def test03(self):
        # 第一种
        # cx_Oracle.init_oracle_client(config_dir="/Users/tiejunzhu/Desktop/profile/instantclient_12_2")
        cx.init_oracle_client(lib_dir="/Users/tiejunzhu/Desktop/profile/instantclient_12_2")
        # dsn = cx.makedsn('192.168.66.115', '1521', 'orcl')
        # conn = cx.connect('credit', 'test201988', dsn)
        conn = cx.connect("credit", "test201988", "192.168.66.115:1521/orcl")
        # con = cx_Oracle.connect(user="credit", password="test201988", dsn="192.168.66.115:1521/orcl")
        cursor = conn.cursor()  # 创建游标
        cursor.execute("SELECT * FROM CREDIT_APPLY")  # 执行sql语句
        data = cursor.fetchone()  # 获取一条数据
        print(data)  # 打印数据
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        # 第二种
        # con = cx.connect('root/root123@127.0.0.1:1521/orcl')
        # 第三种
        # dsn = cx.makedsn('127.0.0.1', '1521', 'orcl')
        # connection = cx.connect('root', 'root123', dsn)

    def test04(self):
        print(randomEnglishInt(32).upper())


    def test05(self):
        root_file = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('test')[0], "result", "test.txt")
        file = open(file=root_file, mode="r", encoding="utf-8")
        list = file.readlines()
        for i in list:
            li = i.split("\t")
            print(li)
            print(li[0])
            print(li[1])
            print(li[2])

    def test06(self):
        user = "system"
        password = "system"
        database = "192.168.66.115:1521/orcl"
        oracleUtil = OracleUtil(user, password, database)
        oracleUtil.connect()
        print(oracleUtil.selectAllTableCount())

    def test07(self):
        t = time.time()
        print(str(int(t)))

    def test08(self):
        sql = "select t.table_name tableName, t.NUM_ROWS, f.comments comments from dba_tables t inner join dba_tab_comments f on t.table_name = f.table_name where t.TABLE_NAME not like '%$%' and f.COMMENTS is not null and t.NUM_ROWS > 0 and f.OWNER in ('BJYH_MEITUANSHF', 'CREDIT')"
        user = "system"
        password = "system"
        database = "192.168.66.115:1521/orcl"
        oracleUtil = OracleUtil(user, password, database)
        oracleUtil.connect()
        result_list = oracleUtil.selectSql(sql)
        for result_tuple in result_list:
            print(result_tuple)

    def test09(self):
        host_dict = {
            "host": "192.168.66.115",
            "username": "root",
            "password": "yrjk%!123098",
            "port": 22
        }
        sshConn = SSHUtil(host_dict)
        sshConn.connect()
        root_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "20210604.html")
        print(root_file)
        sshConn.download("/app/oracle/product/12.2.0/dbhome_1/bin/202105271920.html", root_file)
        sshConn.close()


    def test10(self):
        list_temp = []

        root_file = os.path.join(os.path.abspath(os.path.dirname(__file__)).split("test")[0], "result", "A")
        print(root_file)
        file = open(file=root_file, mode="r", encoding="utf-8")
        list = file.readlines()
        file.close()
        for i in list:
            li = i.split("\t")[1]
            if i not in list_temp:
                list_temp.append(li)
            else:
                print(file)
                print(i)

        root_file_1 = os.path.join(os.path.abspath(os.path.dirname(__file__)).split("test")[0], "result", "B")
        print(root_file_1)
        file_1 = open(file=root_file_1, mode="r", encoding="utf-8")
        list_1 = file_1.readlines()
        file_1.close()
        for i in list_1:
            li = i.split("\t")[1]
            if i not in list_temp:
                list_temp.append(li)
            else:
                print(root_file_1)
                print(i)

        root_file_2 = os.path.join(os.path.abspath(os.path.dirname(__file__)).split("test")[0], "result", "C")
        print(root_file_2)
        file_2 = open(file=root_file_2, mode="r", encoding="utf-8")
        list_2 = file_2.readlines()
        file_2.close()
        for i in list_2:
            li = i.split("\t")[1]
            if i not in list_temp:
                list_temp.append(li)
            else:
                print(root_file_2)
                print(i)

        root_file_3 = os.path.join(os.path.abspath(os.path.dirname(__file__)).split("test")[0], "result", "D")
        print(root_file_3)
        file_3 = open(file=root_file_3, mode="r", encoding="utf-8")
        list_3 = file_3.readlines()
        file_3.close()
        for i in list_3:
            li = i.split("\t")[1]
            if i not in list_temp:
                list_temp.append(li)
            else:
                print(root_file_3)
                print(i)

        sql_1 = "select count(1) from CREDIT.CREDIT_APPLY where  CERTIFICATE_NO = '{}'"
        sql_2 = "select count(1) from CREDIT.CREDIT_CUSTOMER_LIMIT_INFO where  CERTIFICATE_NO = '{}'"
        user = "system"
        password = "system"
        database = "192.168.66.115:1521/orcl"
        oracleUtil = OracleUtil(user, password, database)
        oracleUtil.connect()
        i_list = []
        for i in list_temp:
            k = oracleUtil.selectSql(sql_1.format(i))[0][0]
            j = oracleUtil.selectSql(sql_2.format(i))[0][0]
            if k != 1:
                print(k)
                print(i)
                i_list.append(i)
            if j != 1:
                print(j)
                print(i)
                i_list.append(i)
        print(i_list)

    def test12(self):
        sql_credit = "select 'truncate table CREDIT.'||TABLE_NAME||';' from all_tables where TABLE_NAME like 'CREDIT_STD%' and OWNER='CREDIT'"
        sql_bjyh = "select 'truncate table BJYH_MEITUANSHF.'||TABLE_NAME||';' from all_tables where TABLE_NAME like 'MTSHF%' and OWNER='BJYH_MEITUANSHF'"
        user = "system"
        password = "system"
        database = "192.168.66.115:1521/orcl"
        oracleUtil = OracleUtil(user, password, database)
        oracleUtil.connect()
        result = oracleUtil.selectSql(sql_bjyh)
        for i in result:
            print(i[0])

    def test13(self):
        root_file = os.path.join(os.path.abspath(os.path.dirname(__file__)).split("test")[0], "test", "test")
        print(root_file)
        file = open(file=root_file, mode="r", encoding="utf-8")
        jsonRes = json.loads(file.read())
        file.close()
        user = "system"
        password = "system"
        database = "192.168.66.115:1521/orcl"
        oracleUtil = OracleUtil(user, password, database)
        oracleUtil.connect()
        sql = "select count(*) from CREDIT.CREDIT_APPLY where  CERTIFICATE_NO = '{}'"
        for i in jsonRes["billSyncLoanDetailDtoList"]:
            certificateId = i["borrower"]["certificateId"]
            count = oracleUtil.selectSql(sql.format(certificateId))[0][0]
            print("{} : {}".format(certificateId, count))
            if count != 1:
                print(certificateId)





