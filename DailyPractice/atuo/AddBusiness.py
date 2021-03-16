import requests






addurl = "http://192.168.8.32:8097/tsnShipping/shipping/export/input/saveBaseInfoAndSubmit"
addheaders = {
    "cookie" : "JSESSIONID=BAF80590428726D30DD0528537FB2B2A; StimulsoftWebViewerExportSettingsOpeningGroups=%7B%22SavingReportGroup%22%3Atrue%2C%22PageRangeGroup%22%3Atrue%2C%22SettingsGroup%22%3Afalse%7D; StimulsoftWebViewerExportSettingsPdf=%7B%22PageRange%22%3A%22All%22%2C%22ImageResolution%22%3A%22100%22%2C%22ImageCompressionMethod%22%3A%22Jpeg%22%2C%22ImageQuality%22%3A%220.75%22%2C%22EmbeddedFonts%22%3Atrue%2C%22ExportRtfTextAsImage%22%3Afalse%2C%22PdfACompliance%22%3Afalse%2C%22OpenAfterExport%22%3Afalse%2C%22AllowEditable%22%3A%22No%22%2C%22PasswordInputUser%22%3A%22%22%2C%22PasswordInputOwner%22%3A%22%22%2C%22KeyLength%22%3A%22Bit40%22%2C%22UseDigitalSignature%22%3Afalse%2C%22GetCertificateFromCryptoUI%22%3Afalse%2C%22UserAccessPrivileges%22%3A%22PrintDocument%2C%20ModifyContents%2C%20CopyTextAndGraphics%2C%20AddOrModifyTextAnnotations%22%7D; StiMobileDesignerDictionarySettings=%7B%22createFieldOnDoubleClick%22%3Afalse%2C%22createLabel%22%3Afalse%2C%22useAliases%22%3Afalse%7D; cultureName=Chinese%20%28Simplified%29; login_token=4c77b497-2899-4147-9efb-667cdebe517d; userId=admin_qs; userName=admin_qs"
}



# response = requests.post(url=url,headers=headers,json=FCL_josn)
# print(response.status_code)
# print(response.text)



def AddBusiness(url,headers):
    businesstype = input("输入业务类型:")
    businessno = input("输入业务编号:")

    LCL_josn = {"baseBean": {"businessNo": businessno,
                             "consignor": 79,
                             "consignorDescribe": "39 LONGTANG ROAD , DIPU STREET,ANJI TOWN,HUZHOU CITY,ZHEJIANG PROVINCE.ANJI BOYANG FURNITURE CO.,LTD.",
                             "consignee": "ANJI MAOCHANG FURNITURE CO. China",
                             "notifications": "HANGZHOU XINLONG CHEMICAL CO.,LTD YIPENG SPRING ", "client": "",
                             "receivingAddress": "", "transportClause": "05", "freightClause": "02",
                             "departurePort": 2759, "transferPort": "", "destinationPort": 2744, "serviceLineId": 6,
                             "destination": "", "estimateShipping": "2020-05-30", "shippingName": "",
                             "voyage": "", "billIssuePlace": "", "billType": "", "billCount": "THREE", "billMode": "2",
                             "billAgentFlag": "", "shippingCompany": "", "shippingCompanyAppointNo": "", "payBill": "",
                             "deliveryType": "02", "doorPackingType": "", "innerBoxType": "02", "entryType": "1",
                             "warehouseId": 18, "warehouseAddress": "杭州市下城区石桥路", "warehouseContacts": "诸葛亮",
                             "warehousePhone": "17687222111", "id": 2048, "customsConfirmButton": "",
                             "downloadDocumentButton": "", "businessType": "02", "assignDispatchersId": "",
                             "bookingStatus": "01",
                             "trailerStatus": "", "documentStatus": "", "customsStatus": "", "entryDeclareType": "",
                             "arriveStatus": "", "customerConfirmStatus": "", "downloadBillStatus": "",
                             "consignorName": "博扬", "consignorCode": "AJBY", "departurePortName": "SHANGHAI,CHINA ",
                             "transferPortName": "", "destinationPortName": "NINGBO,CHINA ",
                             "departurePortCode": "CNSHA", "transferPortCode": "", "destinationPortCode": "CNNBO",
                             "shippingCompanyName": "", "shippingCompanyCode": "", "serviceLineCode": "MIDDLE EAST",
                             "serviceLineName": "",
                             "serviceLineNameCn": "中东线", "childFlag": "", "supplierCustomsBrokerId": "",
                             "supplierCustomsBrokerName": "", "supplierCustomsBrokerCode": "",
                             "warehouseCode": "HAIZHU", "warehouseName": "海珠杭州仓储中心",
                             "destinationCountryEnName": "CHINA", "customerNo": "79", "customerCode": "AJBY",
                             "customerName": "安吉博扬家居有限公司", "salesPersonnelName": "", "customerPersonnelName": "客服1",
                             "businessPersonnelName": "", "salesPersonnelId": "", "customerPersonnelId": "service1",
                             "businessPersonnelId": ""}, "containerList":[{"containerId": "", "containerTypeCode": "",
                             "containerTypeName": ""}],"merchandiseBean": {"cnGoodsName": "", "enGoodsName": "englishname",
                             "shippingMarks": "maitou","hsCode": "", "packNo": 3, "unitId": "374", "grossWeight": 300,
                             "volume": 3, "mbL": "", "exitPort": "", "": "", "atd": "", "wharfId": "", "portOpenDate": "",
                             "portCloseDate": "", "customsCloseDate": "", "orderCloseDate": "", "jamsEms": "",
                             "remark": "", "unitCode": "SU", "unitName": "SCSES"}}

    FCL_josn = {"baseBean": {"businessNo": businessno,
                             "consignor": 79,
                             "consignorDescribe": "39 LONGTANG ROAD , DIPU STREET,ANJI TOWN,HUZHOU CITY,ZHEJIANG PROVINCE.ANJI BOYANG FURNITURE CO.,LTD.",
                             "consignee": "DRAGAN C.DUMITRU\nIMPORTS-EXPORTS OF CLOTHING SHOES \nAND RELEVANT ACCESSORIES\n44 ROUMPESI STR ATHENS P.O 11744 GREECE\nID:169907254\n+30 6942474718 \nEMAIL:LINLONG116688@GMAIL.COM",
                             "notifications": "ANJI MAOCHANG FURNITUREovince, China", "client": "",
                             "receivingAddress": "", "transportClause": "05", "freightClause": "02",
                             "departurePort": 2759,
                             "transferPort": "", "destinationPort": 2744, "serviceLineId": 6, "destination": "",
                             "estimateShipping": "2020-04-30", "shippingName": "", "voyage": "", "billIssuePlace": "",
                             "billType": "", "billCount": "THREE", "billMode": "1", "billAgentFlag": "",
                             "shippingCompany": "", "shippingCompanyAppointNo": "", "payBill": "", "deliveryType": "01",
                             "doorPackingType": "01", "innerBoxType": "", "entryType": "1", "warehouseId": "",
                             "warehouseAddress": "", "warehouseContacts": "", "warehousePhone": "", "id": 2053,
                             "customsConfirmButton": "",
                             "downloadDocumentButton": "", "businessType": "01", "assignDispatchersId": "",
                             "bookingStatus": "01", "trailerStatus": "", "documentStatus": "", "customsStatus": "",
                             "entryDeclareType": "", "arriveStatus": "", "customerConfirmStatus": "",
                             "downloadBillStatus": "", "consignorName": "博扬", "consignorCode": "AJBY",
                             "departurePortName": "SHANGHAI,CHINA ", "transferPortName": "",
                             "destinationPortName": "NINGBO,CHINA ", "departurePortCode": "CNSHA",
                             "transferPortCode": "", "destinationPortCode": "CNNBO", "shippingCompanyName": "",
                             "shippingCompanyCode": "", "serviceLineCode": "MIDDLE EAST", "serviceLineName": "",
                             "serviceLineNameCn": "中东线", "childFlag": "", "supplierCustomsBrokerId": "",
                             "supplierCustomsBrokerName": "", "supplierCustomsBrokerCode": "", "warehouseCode": "",
                             "warehouseName": "", "destinationCountryEnName": "CHINA", "customerNo": "79",
                             "customerCode": "AJBY", "customerName": "安吉博扬家居有限公司", "salesPersonnelName": "",
                             "customerPersonnelName": "客服1", "businessPersonnelName": "", "salesPersonnelId": "",
                             "customerPersonnelId": "service1","businessPersonnelId": ""}, "containerList": [{
                             "containerId": 30, "containerCount": 2, "containerTypeCode": "20GP", "containerTypeName": "20GP"}],
                             "merchandiseBean": {"cnGoodsName": "", "enGoodsName": "englishname", "shippingMarks": "maitou",
                             "hsCode": "", "packNo": 3, "unitId": "357", "grossWeight": 300, "volume": 3,
                             "mbL": "", "exitPort": "", "": "", "atd": "", "wharfId": "", "portOpenDate": "",
                             "portCloseDate": "", "customsCloseDate": "", "orderCloseDate": "", "jamsEms": "",
                             "remark": "", "unitCode": "PE", "unitName": "PLTS"}}

    DDC_josn = {"baseBean":{"businessNo":businessno,
                            "consignor":79,"consignorDescribe":"39 LONGTANG ROAD , DIPU STREET,ANJI TOWN,HUZHOU CITY,ZHEJIANG PROVINCE.ANJI BOYANG FURNITURE CO.,LTD.",
                            "consignee":"ANJI MAOCHANG FURNITURE CO., China","notifications":"WUFANGYUAN LTD.\n1501(105), ","client":"","receivingAddress":"",
                            "transportClause":"03","freightClause":"01","departurePort":2759,"transferPort":"","destinationPort":2744,"serviceLineId":6,"destination":"",
                            "estimateShipping":"2020-05-30","shippingName":"","voyage":"","billIssuePlace":"","billType":"","billCount":"THREE","billMode":"1","billAgentFlag":"",
                            "shippingCompany":"","shippingCompanyAppointNo":"","payBill":"","deliveryType":"01","doorPackingType":"02","innerBoxType":"","entryType":"2",
                            "warehouseId":"","warehouseAddress":"","warehouseContacts":"","warehousePhone":"","id":2064,"customsConfirmButton":"","downloadDocumentButton":"",
                            "businessType":"04","assignDispatchersId":"","bookingStatus":"01","trailerStatus":"","documentStatus":"","customsStatus":"","entryDeclareType":"",
                            "arriveStatus":"","customerConfirmStatus":"","downloadBillStatus":"","consignorName":"博扬","consignorCode":"AJBY","departurePortName":"SHANGHAI,CHINA ",
                            "transferPortName":"","destinationPortName":"NINGBO,CHINA ","departurePortCode":"CNSHA","transferPortCode":"","destinationPortCode":"CNNBO",
                            "shippingCompanyName":"","shippingCompanyCode":"","serviceLineCode":"MIDDLE EAST","serviceLineName":"","serviceLineNameCn":"中东线","childFlag":"",
                            "supplierCustomsBrokerId":"","supplierCustomsBrokerName":"","supplierCustomsBrokerCode":"","warehouseCode":"","warehouseName":"",
                            "destinationCountryEnName":"CHINA","customerNo":"79","customerCode":"AJBY","customerName":"安吉博扬家居有限公司","salesPersonnelName":"",
                            "customerPersonnelName":"","businessPersonnelName":"商务人员2","salesPersonnelId":"","customerPersonnelId":"","businessPersonnelId":"business2"},
                            "containerList":[{"containerId":30,"containerCount":2,"containerTypeCode":"20GP","containerTypeName":"20GP"}],"merchandiseBean":{"cnGoodsName":"",
                            "enGoodsName":"englishname","shippingMarks":"maitou","hsCode":"","packNo":3,"unitId":"351","grossWeight":300,"volume":3,"mbL":"","exitPort":"",
                            "":"","atd":"","wharfId":"","portOpenDate":"","portCloseDate":"","customsCloseDate":"",
                            "orderCloseDate":"","jamsEms":"","remark":"","unitCode":"NE","unitName":"UPKDS"}}

    if businesstype == "1":
        response = requests.post(url=url, headers=headers, json=FCL_josn)
        print(response.status_code)
        print(response.text)

    if businesstype == "2":
        response = requests.post(url=url, headers=headers, json=LCL_josn)
        print(response.status_code)
        print(response.text)

    if businesstype == "3":
        response = requests.post(url=url, headers=headers, json=DDC_josn)
        print(response.status_code)
        print(response.text)







if __name__ == '__main__':
    AddBusiness(addurl, addheaders)






