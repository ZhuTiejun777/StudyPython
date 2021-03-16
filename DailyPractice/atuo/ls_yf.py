import pymysql
import requests

url_yffy = "http://122.224.230.26:20054/tsnShipping/shipping/export/feeout/saveOrUpdate"
url_ysfy = "http://122.224.230.26:20054/tsnShipping/shipping/export/feein/saveOrUpdate"
headers = {
    "Cookie": "JSESSIONID=E4D56E8503CCD0E27F328D19491B4871; login_token=cca4f2b2-8c77-4992-9857-dc53bbf56021; userId=qs_opt1; userName=%E6%93%8D%E4%BD%9C%E5%91%98A"
}

mysql_dist = {
    "host": "192.168.3.110", "port": 3306,
    "user": "root", "password": "zjport",
    "database": "tsn", "charset": "utf8"
}

businessNo = 'SE20010700033'


def res_post(url, headers, json, text):
    print(text)
    response = requests.post(url=url, headers=headers, json=json)
    print(response.status_code)
    print(response.text)


def get_baseid(db, sql):
    connect = pymysql.connect(host=db['host'], port=db['port'],
                              user=db['user'], password=db['password'],
                              database=db['database'], charset=db['charset'])
    cursor = connect.cursor()
    cursor.execute(sql)
    base_id = cursor.fetchall()
    cursor.close()
    connect.close()
    print(base_id[0][0])
    return base_id[0][0]


baseid_sql = "select id from tsn_shipping_export_base where business_no = '" + businessNo + "'"

baseid = get_baseid(mysql_dist, baseid_sql)

yffy_json = {"baseId": baseid,
             "feeOuts": [
                 {
                     "id": "",
                     "chargeId": 30,
                     "chargeName": "多联报关费",
                     "currency": "RMB",
                     "currencyRate": 1,
                     "qty": 10,
                     "price": 10,
                     "amount": 100,
                     "clientId": "",
                     "clientCode": "",
                     "clientName": "",
                     "clientType": "",
                     "supplier": "41-4",
                     "supplierId": 41,
                     "supplierCode": "3302980205",
                     "supplierName": "DUBNAMECNSHORT",
                     "supplierType": "4",
                     "remark": "易豹报关费",
                     "unit": "箱"
                 },
                 {
                     "id": "",
                     "chargeId": 50,
                     "chargeName": "进仓费",
                     "currency": "USD",
                     "currencyRate": 6.8,
                     "qty": 10,
                     "price": 1,
                     "amount": 10,
                     "clientId": "",
                     "clientCode": "",
                     "clientName": "",
                     "clientType": "",
                     "supplier": "18-2",
                     "supplierId": 18,
                     "supplierCode": "HAIZHU",
                     "supplierName": "海珠杭州仓储中心",
                     "supplierType": "2",
                     "remark": "海珠仓库",
                     "unit": "20"
                 },
                 {
                     "id": "",
                     "chargeId": 87,
                     "chargeName": "箱单费",
                     "currency": "RMB",
                     "currencyRate": 1,
                     "qty": 1,
                     "price": 10,
                     "amount": 10,
                     "clientId": "",
                     "clientCode": "",
                     "clientName": "",
                     "clientType": "",
                     "supplier": "89-1",
                     "supplierId": 89,
                     "supplierCode": "91310115MA1HA5651R",
                     "supplierName": "骝马名称",
                     "supplierType": "1",
                     "remark": "骝马运力",
                     "unit": "40"
                 },
                 {
                     "id": "",
                     "chargeId": 140,
                     "chargeName": "订舱费",
                     "currency": "USD",
                     "currencyRate": 6.8,
                     "qty": 1,
                     "price": 1,
                     "amount": 1,
                     "clientId": "",
                     "clientCode": "",
                     "clientName": "",
                     "clientType": "",
                     "supplier": "52-3",
                     "supplierId": 52,
                     "supplierCode": "JCGJ",
                     "supplierName": "锦程国际订舱有限公司",
                     "supplierType": "3",
                     "remark": "锦城订舱",
                     "unit": "40"
                 }],
             "rmbAmount": 110,
             "usdAmount": 11,
             "optFlag": "SUBMIT"
             }

xzyffy_str = "新增应付费用"

res_post(url_yffy, headers, yffy_json, xzyffy_str)
