import random
import pymysql

# num = random.randint(0,10000)
#
# businessNo = "SE20010600042"
#
# print(businessNo[-5:])
# print(type(businessNo[-5:]))
#
# MB_L = "MBL" + businessNo[-5:]
# print(MB_L)

mysql_dist = {
    "host":"192.168.3.110","port":3306,
    "user":"root","password":"zjport",
    "database":"tsn","charset":"utf8"
}

businessNo = "SE20010700028"

def get_baseid(db, sql):
    connect = pymysql.connect(host=db['host'], port=db['port'],
                              user=db['user'], password=db['password'],
                              database=db['database'], charset=db['charset'])
    cursor = connect.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    connect.close()

    # return base_id

baseid_sql = "select id from tsn_shipping_export_base where business_no = '" + businessNo + "'"

# baseid = get_baseid(mysql_dist, baseid_sql)
# print(baseid)

tuple_sql = ((242,),)

print(tuple_sql[0][0])
print(type(tuple_sql[0][0]))