import pymysql
import requests

url_ysfy = "http://122.224.230.26:20054/tsnShipping/shipping/export/feein/saveOrUpdate"
headers = {
    "Cookie": "JSESSIONID=31627F87F63FC411EA58219D33C8E0DB; login_token=cca4f2b2-8c77-4992-9857-dc53bbf56021; userId=qs_opt1; userName=%E6%93%8D%E4%BD%9C%E5%91%98A"
}
mysql_dist = {
    "host": "192.168.3.110", "port": 3306,
    "user": "root", "password": "zjport",
    "database": "tsn", "charset": "utf8"
}

businessNo = 'SE20010700034'


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

#浙江华丰新材料股份有限公司
ysfyhf_json = {"baseId":baseid,
             "feeIns":
                 [{"id":"",
                   "chargeId":22,
                   "chargeName":"出口查验费",
                   "currency":"RMB",
                   "currencyRate":1,
                   "qty":1,
                   "price":10,
                   "amount":10,
                   "clientId":83,
                   "clientCode":"HUFON",
                   "clientName":"浙江华丰新材料股份有限公司 ",
                   "clientType":1,
                   "supplier":"",
                   "supplierId":"",
                   "supplierCode":"",
                   "supplierName":"",
                   "supplierType":"",
                   "remark":"1111",
                   "unit":"箱"},
                  {"id":"",
                   "chargeId":24,
                   "chargeName":"电放费",
                   "currency":"USD",
                   "currencyRate":6.8,
                   "qty":10,
                   "price":1,
                   "amount":10,
                   "clientId":83,
                   "clientCode":"HUFON",
                   "clientName":"浙江华丰新材料股份有限公司 ",
                   "clientType":1,
                   "supplier":"",
                   "supplierId":"",
                   "supplierCode":"",
                   "supplierName":"",
                   "supplierType":"",
                   "remark":"2222",
                   "unit":"车"}],
             "rmbAmount":10,
             "usdAmount":10,
             "optFlag":"SUBMIT"}

#安徽轻工国际贸易有限公司
ysfyqg_json = {"baseId":baseid,
             "feeIns":[{
                 "id":"",
                 "chargeId":67,
                 "chargeName":"内装费",
                 "currency":"RMB",
                 "currencyRate":1,
                 "qty":1,
                 "price":10,
                 "amount":10,
                 "clientId":81,
                 "clientCode":"HT0001A",
                 "clientName":"安徽轻工国际贸易有限公司",
                 "clientType":1,
                 "supplier":"",
                 "supplierId":"",
                 "supplierCode":"",
                 "supplierName":"",
                 "supplierType":"",
                 "remark":"1111",
                 "unit":"车"},
                 {"id":"",
                  "chargeId":53,
                  "chargeName":"截关费",
                  "currency":"USD",
                  "currencyRate":6.8,
                  "qty":10,
                  "price":1,
                  "amount":10,
                  "clientId":81,
                  "clientCode":"HT0001A",
                  "clientName":"安徽轻工国际贸易有限公司",
                  "clientType":1,
                  "supplier":"",
                  "supplierId":"",
                  "supplierCode":"",
                  "supplierName":"",
                  "supplierType":"",
                  "remark":"2222",
                  "unit":"箱"}],
             "rmbAmount":10,
             "usdAmount":10,
             "optFlag":"SUBMIT"}

xzyffy_str = "新增应收费用"

res_post(url_ysfy, headers, ysfyqg_json, xzyffy_str)