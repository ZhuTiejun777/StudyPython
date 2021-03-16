import requests
import re

#cookie
cookies = {
    "name": "login_token",
    "value": "9d17e4a6-4408-4dcc-a9fc-c561a3417647",
}

#header
headers = {
    "Cookie": "JSESSIONID=E637F80782359421C0D13F027B9CB853; login_token=4bc51647-f8fb-46b9-972d-790eff7cb7f0; userId=admin_qs; userName=admin_qs; sidebarStatus=1"
}

#数据库配置
mysql_dist = {
    "host": "192.168.3.110", "port": 3306,
    "user": "root", "password": "zjport",
    "database": "tsn", "charset": "utf8"
}

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

#--------------------------------------------------------------------------------------------------------------
hqywbh_str = "获取业务编号"

#获取业务编号url
url_hqywbh = 'http://122.224.230.26:20054/tsnShipping/shipping/export/inputBill/createBusinessNo'

#获取业务编号并打印
businessNo = get_businessNo(url_hqywbh,headers,hqywbh_str)
#--------------------------------------------------------------------------------------------------------------
jbxx_str = "暂存基本信息"

#暂存基本信息url
url_zcjbxx = "http://122.224.230.26:20054/tsnShipping/shipping/export/input/saveBaseInfoAndSubmit"

#暂存基本信息json
jbxx_json = {"baseBean":
                 {"consignor":88,
                  "consignorDescribe":"YUANHUI ROOM701,NO.86 QINGCHUN ROAD,DOWNTOWN DISTRICT,HANGZHOU",
                  "consignee":"张三",
                  "notifications":"李四",
                  "client":"YUANHUI",
                  "receivingAddress":"",
                  "transportClause":"01",
                  "freightClause":"01",
                  "departurePort":2759,
                  "wharfId":"",
                  "transferPort":"",
                  "destinationPort":2744,
                  "destination":"",
                  "exitPort":"nb",
                  "estimateShipping":"2020-03-07",
                  "billIssuePlace":"",
                  "billType":"01",
                  "billCount":"THREE",
                  "payBill":"",
                  "businessInformation":"",
                  "id":"",
                  "customsConfirmButton":"",
                  "downloadDocumentButton":"",
                  "businessType":"01",
                  "assignDispatchersId":"",
                  "bookingStatus":"",
                  "trailerStatus":"",
                  "documentStatus":"",
                  "customsStatus":"",
                  "arriveStatus":"",
                  "customerConfirmStatus":"",
                  "downloadBillStatus":"",
                  "consignorName":"YUANHUI",
                  "consignorCode":"YUANHUI",
                  "departurePortName":"SHANGHAI",
                  "transferPortName":"",
                  "destinationPortName":"NINGBO",
                  "departurePortCode":"CNSHA",
                  "transferPortCode":"",
                  "destinationPortCode":"CNNBO",
                  "wharfName":"",
                  "wharfCode":"",
                  "supplierCustomsBrokerCode":"9133010035",
                  "businessNo":businessNo,
                  "customerNo":88,
                  "customerCode":"YUANHUI",
                  "customerName":"YUANHUI"},
             "hbaseBean":[],
             "containerList":[{"containerId":51,"containerCount":2,"containerTypeCode":"40OT","containerTypeName":"40OT"}],"merchandiseBean":{"cnGoodsName":"橙子","enGoodsName":"chengzi","shippingMarks":"null","hsCode":"","packNo":2,"unitId":"341","grossWeight":2,"netWeight":2,"volume":2,"remark":"","unitCode":"DI","unitName":"IDRMS"}}

#暂存基本信息请求
res_post(url_zcjbxx,headers,jbxx_json,jbxx_str)
#--------------------------------------------------------------------------------------------------------------
dcxx_str = "暂存订舱信息"

#暂存订舱信息url
url_zcdcxx = "http://122.224.230.26:20054/tsnShipping/shipping/export/input/saveTransportInfo?businessNo=" + businessNo

#暂存订舱信息
dcxx_json = {"bookShippingCode":"pass",
             "mbL":"pass",
             "hbL":"pass",
             "shippingCompany":219,
             "soCode":"pass",
             "soDate":"2020-03-07 00:00:00",
             "shippingName":"pass",
             "bookingAgentCode":52,
             "voyage":"pass",
             "":"",
             "portOpenDate":"",
             "portCloseDate":"",
             "customsCloseDate":"",
             "orderCloseDate":"",
             "etd":"",
             "atd":"",
             "destinationPortApply":"",
             "serviceLineId":"",
             "jamsEms":"",
             "shippingCompanyName":"川崎汽船",
             "shippingCompanyCode":"KLINE","serviceLineCode":"",
             "serviceLineName":"",
             "serviceLineNameCn":"",
             "bookingAgentName":"锦程国际订舱有限公司"}

#暂存订舱信息请求
res_post(url_zcdcxx,headers,dcxx_json,dcxx_str)
#--------------------------------------------------------------------------------------------------------------
# ddxx_str = "暂存调度信息"

