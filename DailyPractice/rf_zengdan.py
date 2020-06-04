import pymysql
import requests
import re

#cookie
cookies = {
    "name": "login_token",
    "value": "9d17e4a6-4408-4dcc-a9fc-c561a3417647",
}

#header
headers = {
    "Cookie": "JSESSIONID=40A7A5A3050ED756B8810FBE2117A324; login_token=34098aa7-a353-4e2e-a725-fe3df0fc84c6; userId=admin_qs; userName=admin_qs"
}

#数据库配置
mysql_dist = {
    "host": "192.168.3.110", "port": 3306,
    "user": "root", "password": "zjport",
    "database": "tsn", "charset": "utf8"
}

#获取业务编号
def get_businessNo(url, headers, text):
    print(text)
    response = requests.post(url=url, headers=headers)
    print(text, response.status_code)
    print(text, response.text)
    businessNo = re.search(r"SETEST\d{11}", response.text).group()
    print("业务编号：", businessNo)
    print("-"*50)
    return businessNo

#请求方法
def res_post(url, headers, json, text):
    print(text)
    response = requests.post(url=url, headers=headers, json=json)
    print(text, response.status_code)
    print(text, response.text)
    print("-" * 50)

#从数据库中获取业务编号对应的base_id
def get_baseid(db, sql):
    connect = pymysql.connect(host=db['host'], port=db['port'],
                              user=db['user'], password=db['password'],
                              database=db['database'], charset=db['charset'])
    cursor = connect.cursor()
    cursor.execute(sql)
    base_id = cursor.fetchall()
    cursor.close()
    connect.close()
    print("base_id:", base_id[0][0])
    print("-" * 50)
    return base_id[0][0]
#--------------------------------------------------------------------------------------------------------------
hqywbh_str = "获取业务编号"

#获取业务编号url
url_ywbh = "http://122.224.230.26:20054/tsnShipping/shipping/export/inputBill/createBusinessNo"

#获取业务编号并打印
businessNo = get_businessNo(url_ywbh, headers, hqywbh_str)

#--------------------------------------------------------------------------------------------------------------
jbxx_str = "提交基本信息"

#提交基本信息参数
jbxx_json = {"baseBean":
                 {"consignor": "83",
                  "supplierCustomsBrokerCode": "33019661N9",
                  "consignorDescribe": "ZHEJIANG HUFON NEW MATERIALS CO., LTD.  NO.1688 KAIFAQU ROAD, RUIAN ECONOMIC DEVELOPMENT ZONE, ZHEJIANG, CHINA",
                  "consignee": " 收货人",
                  "notifications": " 通知人",
                  "client": "HUFON",
                  "transportClause": "01",
                  "freightClause": "01",
                  "departurePort": "2",
                  "wharfId": 9,
                  "transferPort": "6641",
                  "destinationPort": "10071",
                  "exitPort": "nb",
                  "receivingAddress": "收货地",
                  "destination": "目的地",
                  "bookingAgent": "52",
                  "estimateShipping": "2020-03-12",
                  "billType": "01",
                  "billCount": 5,
                  "billIssuePlace": "签发地",
                  "businessInformation": "",
                  "id": 249,
                  "customsConfirmButton": "",
                  "downloadDocumentButton": "1",
                  "businessType": "01",
                  "assignDispatchersId": "",
                  "bookingStatus": "03",
                  "trailerStatus": "",
                  "documentStatus": "",
                  "customsStatus": "W",
                  "arriveStatus": "",
                  "customerConfirmStatus": "",
                  "consignorName": "华丰新材料",
                  "departurePortName": "ningbo1",
                  "transferPortName": "Vancouver",
                  "destinationPortName": "NEW YORK",
                  "consignorCode": "HUFON",
                  "departurePortCode": "CNNGB",
                  "transferPortCode": "YVR",
                  "destinationPortCode": "LGA",
                  "bookingAgentName": "锦程国际订舱有限公司",
                  "wharfName": "YSSQ",
                  "wharfCode": "YSSQ",
                  "businessNo": businessNo,
                  "customerNo": "83",
                  "customerCode": "HUFON",
                  "customerName": "浙江华丰新材料股份有限公司 "},
             "hbaseBean": [],
             "containerList": [
                 {"containerId": 50,
                  "containerCount": 5,
                  "containerTypeCode": "40FR",
                  "containerTypeName": "40FR"}],
             "merchandiseBean":
                 {"cnGoodsName": "中文品名",
                  "enGoodsName": "YWPM",
                  "shippingMarks": "唛头",
                  "packNo": 5,
                  "grossWeight": 5,
                  "volume": 5,
                  "remark": "备注",
                  "unitId": "31",
                  "unitCode": "PLT",
                  "unitName": "PALLETS"}}

#提交基本信息url
url_jbxx_tj = "http://122.224.230.26:20054/tsnShipping/shipping/export/input/saveBaseInfoAndSubmit"

#提交基本信息并打印结果
res_post(url_jbxx_tj, headers, jbxx_json, jbxx_str)
#--------------------------------------------------------------------------------------------------------------
dcqr_str = "订舱确认"

#订舱确认请求参数更改
bookShippingCode = "DCBH" + businessNo[-7:]
MBL = "MBL" + businessNo[-7:]
HBL = "HBL" + businessNo[-7:]
SOBH = "SOBH" + businessNo[-7:]

#订舱确认请求参数
dcqr_json = {"bookShippingCode": bookShippingCode,
             "mbL": MBL,
             "hbL": HBL,
             "shippingCompany": "239",
             "soCode": SOBH,
             "soDate": "2020-03-31 00:00:00",
             "shippingName": "船名",
             "voyage": "航次",
             "portOpenDate": "2020-03-31 00:00:00",
             "portCloseDate": "2020-03-31 00:00:00",
             "customsCloseDate": "2020-03-31 00:00:00",
             "orderCloseDate": "2020-03-31 00:00:00",
             "etd": "2020-03-31 00:00:00",
             "atd": "2020-03-31 00:00:00",
             "destinationPortApply": "用箱申请",
             "serviceLineId": "2",
             "shippingCompanyName": "中海集运",
             "shippingCompanyCode": "COSCO",
             "serviceLineCode": "SDFS",
             "serviceLineName": "AIOUNIYA",
             "serviceLineNameCn": "艾欧尼亚"
             }

#订舱确认url
url_dcqr = "http://122.224.230.26:20054/tsnShipping/shipping/export/input/saveTransportInfo?businessNo=" + businessNo

#订舱确认并打印结果
res_post(url_dcqr, headers, dcqr_json, dcqr_str)
#--------------------------------------------------------------------------------------------------------------
xzyffy_str = "新增应付费用"

#新增应付费用url
url_yffy = "http://122.224.230.26:20054/tsnShipping/shipping/export/feeout/saveOrUpdate"

#获取base_id的sql
baseid_sql = "select id from tsn_shipping_export_base where business_no = '" + businessNo + "'"

#获取base_id
baseid = get_baseid(mysql_dist, baseid_sql)

#新增应付费用的参数
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

#获取应付费用并打印结果
res_post(url_yffy, headers, yffy_json, xzyffy_str)
#--------------------------------------------------------------------------------------------------------------
xzyffy_str = "新增应收费用"

#新增应收费用并打印
url_ysfy = "http://122.224.230.26:20054/tsnShipping/shipping/export/feein/saveOrUpdate"

# 浙江华丰新材料股份有限公司
ysfyhf_json = {"baseId": baseid,
               "feeIns":
                   [{"id": "",
                     "chargeId": 22,
                     "chargeName": "出口查验费",
                     "currency": "RMB",
                     "currencyRate": 1,
                     "qty": 1,
                     "price": 10,
                     "amount": 10,
                     "clientId": 83,
                     "clientCode": "HUFON",
                     "clientName": "浙江华丰新材料股份有限公司 ",
                     "clientType": 1,
                     "supplier": "",
                     "supplierId": "",
                     "supplierCode": "",
                     "supplierName": "",
                     "supplierType": "",
                     "remark": "1111",
                     "unit": "箱"},
                    {"id": "",
                     "chargeId": 24,
                     "chargeName": "电放费",
                     "currency": "USD",
                     "currencyRate": 6.8,
                     "qty": 10,
                     "price": 1,
                     "amount": 10,
                     "clientId": 83,
                     "clientCode": "HUFON",
                     "clientName": "浙江华丰新材料股份有限公司 ",
                     "clientType": 1,
                     "supplier": "",
                     "supplierId": "",
                     "supplierCode": "",
                     "supplierName": "",
                     "supplierType": "",
                     "remark": "2222",
                     "unit": "车"}],
               "rmbAmount": 10,
               "usdAmount": 10,
               "optFlag": "SUBMIT"}

# 安徽轻工国际贸易有限公司
ysfyqg_json = {"baseId": baseid,
               "feeIns": [{
                   "id": "",
                   "chargeId": 67,
                   "chargeName": "内装费",
                   "currency": "RMB",
                   "currencyRate": 1,
                   "qty": 1,
                   "price": 10,
                   "amount": 10,
                   "clientId": 81,
                   "clientCode": "HT0001A",
                   "clientName": "安徽轻工国际贸易有限公司",
                   "clientType": 1,
                   "supplier": "",
                   "supplierId": "",
                   "supplierCode": "",
                   "supplierName": "",
                   "supplierType": "",
                   "remark": "1111",
                   "unit": "车"},
                   {"id": "",
                    "chargeId": 53,
                    "chargeName": "截关费",
                    "currency": "USD",
                    "currencyRate": 6.8,
                    "qty": 10,
                    "price": 1,
                    "amount": 10,
                    "clientId": 81,
                    "clientCode": "HT0001A",
                    "clientName": "安徽轻工国际贸易有限公司",
                    "clientType": 1,
                    "supplier": "",
                    "supplierId": "",
                    "supplierCode": "",
                    "supplierName": "",
                    "supplierType": "",
                    "remark": "2222",
                    "unit": "箱"}],
               "rmbAmount": 10,
               "usdAmount": 10,
               "optFlag": "SUBMIT"}

#新增应收费用并打印结果
res_post(url_ysfy, headers, ysfyhf_json, xzyffy_str)