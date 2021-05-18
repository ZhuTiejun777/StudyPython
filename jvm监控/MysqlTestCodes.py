import os
import time
from datetime import datetime

import pymysql as pymysql


class ConnMysql(object):

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

    def selectSql(self, selectSqlStr: str):
        cursor = self._connect.cursor()
        try:
            cursor.execute(selectSqlStr)
            data = cursor.fetchall()
            return data
        except Exception as e:
            return None

    def selectTables(self):
        tableList = []
        cursor = self._connect.cursor()
        try:
            cursor.execute("select TABLE_NAME from information_schema.tables where table_schema='creditreport-sit'")
            data = cursor.fetchall()
            for tableName in data:
                tableList.append(tableName[0])
            return tableList
        except Exception as e:
            return None

    def selectTablesCount(self, tableList):
        tableCountDict = {}
        cursor = self._connect.cursor()
        for tableName in tableList:
            cursor.execute("select count(1) from {}".format(tableName))
            tableCount = cursor.fetchall()[0][0]
            tableCountDict[tableName] = tableCount
        return tableCountDict

    def selectTime(self, ):
        cursor = self._connect.cursor()
        cursor.execute("")

    def selectAsyncTaskCount(self, reportCode):
        cursor = self._connect.cursor()
        cursor.execute("select count(1) from async_task where report_code = '{}'".format(reportCode))
        return cursor.fetchall()[0][0]

    def selectAsyncTaskAll(self, reportCode):
        cursor = self._connect.cursor()
        cursor.execute("select state,exec_count from async_task where report_code = '{}'".format(reportCode))
        return cursor.fetchall()[0]

    def selectContent(self, reportCode):
        cursor = self._connect.cursor()
        cursor.execute("select content from origin_report_content where report_code = '{}'".format(reportCode))
        return cursor.fetchall()[0][0]

    @staticmethod
    def compareTable(basisDict, contrastDict):
        diffDict = {}
        for tableName in basisDict:
            if basisDict[tableName] != contrastDict[tableName]:
                # print("{}表存在差异".format(tableName))
                diffDict[tableName] = basisDict[tableName] - contrastDict[tableName]
        return diffDict

    @staticmethod
    def compareResult(b, num):
        #num += 1
        c = {}
        a = {'account_base_info': 19, 'administrative_award_info': 1, 'administrative_penalty_info': 2, 'async_task': 1,
             'bad_debt_summary_info': 1, 'career_info': 5, 'civil_judgment_info': 1, 'common_summary_info': 4,
             'credit_agreement_base_info': 6, 'credit_report_head': 1, 'credit_trans_prompt': 4,
             'debit_card_summary_info': 2, 'enforcement_info': 1, 'housing_fund_pay_info': 1,
             'last_query_record_info': 1, 'living_info': 5, 'loan_summary_info': 3, 'marriage_info': 1,
             'min_living_security_info': 1, 'origin_report_content': 1, 'overdue_summary_info': 5, 'personal_info': 1,
             'phone_info': 5, 'postpaid_bu_info': 2, 'postpay_bu_arrears_summary_info': 1, 'qualification_info': 1,
             'query_record_info': 50, 'query_record_summary_info': 1, 'recent_monthly_performance_info': 10,
             'recent_performance_info': 19, 'recovered_summary_info': 1, 'repay_detail_in_24_month': 384,
             'repay_detail_in_5_year': 766, 'repay_info_in_24_month': 16, 'repay_info_in_5_year': 16,
             'repayment_liability_info': 3, 'repayment_liability_summary_info': 2, 'report_task_content': 1,
             'special_event_info': 2, 'special_trans_info': 3, 'tax_arrears_record': 1}
        for i in a:
            # print(i + "  a:" + str(a[i] * num) + " b:" + str(b[i]))
            if i in b:
                if (a[i] * num) == b[i]:
                    c[i] = a[i] * num - b[i]
                else:
                   print("存在问题表:{}".format(i))
            else:
                print("存在问题表:{}".format(i))
                c[i] = None
        return c

    @staticmethod
    def readResultCSV():
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "BaseData/resultCodes.csv")
        with open(path, mode='r', encoding="UTF-8") as f:
            reportCodes = f.readlines()
            f.close()
        reportCodeList = []
        for line in reportCodes:
            reportCodeList.append(line.strip())
        return reportCodeList

    @staticmethod
    def readContent():
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "BaseData/content.text")
        with open(path, mode='r', encoding="UTF-8") as f:
            content = f.read()
            f.close()
        return content

    def getBeginTime(self):
        reportCodeList = self.readResultCSV()
        cursor = self._connect.cursor()
        cursor.execute("select create_time from async_task WHERE report_code = '{}'".format(reportCodeList[0]))
        return cursor.fetchall()[0][0]

    def getEndTime(self):
        reportCodeList = self.readResultCSV()
        cursor = self._connect.cursor()
        cursor.execute("SELECT update_time from async_task WHERE report_code = '{}'".format(reportCodeList[-1]))
        return cursor.fetchall()[0][0]

    def targetTPS(self):
        startTime = self.getBeginTime()
        print("开始时间:" + str(startTime))
        stopTime = self.getEndTime()
        print("结束时间:" + str(stopTime))
        targetNumber = len(self.readResultCSV()) * 1986
        print("执行指标数:" + str(targetNumber))
        return targetNumber / (float(datetime.timestamp(stopTime)) - float(datetime.timestamp(startTime)))


if __name__ == '__main__':
    dbConfig = {
        "host": "192.168.66.171", "port": 3306,
        "user": "creditrep", "password": "jellyfish1207#",
        "database": "creditreport-sit", "charset": "utf8"
    }
    conn = ConnMysql(dbConfig)
    conn.connect()
    # tableList = conn.selectTables()

    # 现有数据数量
    # basisDict = conn.selectTablesCount(tableList)
    # print("现有数据数量:" + str(basisDict))

    # 原数据数量
    #contrastDict = {'account_base_info': 248064, 'administrative_award_info': 13056, 'administrative_penalty_info': 26112, 'annotation_info': 0, 'async_task': 13083, 'async_task_copy': 28219, 'async_task_detail': 0, 'bad_debt_summary_info': 13056, 'career_info': 65280, 'civil_judgment_info': 13056, 'common_summary_info': 52224, 'credit_agreement_base_info': 78336, 'credit_report_head': 57834, 'credit_trans_prompt': 52224, 'debit_card_summary_info': 26112, 'enforcement_info': 13056, 'ent_act_controller': 4, 'ent_adm_penalty_record': 0, 'ent_annotation_info': 0, 'ent_balance_sheet_2002': 4, 'ent_balance_sheet_2007': 129, 'ent_base_info': 14, 'ent_c_guarantee_sum': 8, 'ent_c_loan_sum': 14, 'ent_certification_record': 0, 'ent_civil_judgment_record': 0, 'ent_controller_info': 4, 'ent_credit_agr_info': 0, 'ent_credit_agr_sum': 0, 'ent_credit_prompt': 14, 'ent_debit_interest': 0, 'ent_debt_history_sum': 168, 'ent_discount_org_sum': 0, 'ent_enforcement_record': 0, 'ent_exempt_insp': 0, 'ent_financing_control': 0, 'ent_green_channel': 0, 'ent_guarantee_account': 6000, 'ent_guarantee_org_sum': 28, 'ent_higher_org_info': 0, 'ent_housing_fund_base_info': 0, 'ent_housing_fund_pay_detail_in_24m': 0, 'ent_icash_flow_stmt_2002': 0, 'ent_icash_flow_stmt_2007': 133, 'ent_id_info': 58, 'ent_income_stmt_2002': 8, 'ent_income_stmt_2007': 133, 'ent_insp_cls_supervise': 0, 'ent_investor_info': 20, 'ent_loan_acc_base_info': 57, 'ent_loan_acc_repay_info': 776, 'ent_loan_acc_st_info': 0, 'ent_loan_repay_liability_sum': 16, 'ent_main_member': 14, 'ent_member_info': 32, 'ent_not_credit_prompt': 14, 'ent_other_c_loan_sum': 0, 'ent_other_uc_loan_sum': 40, 'ent_patent_info': 0, 'ent_permission_record': 0, 'ent_pub_inst_balance_sheet_1997': 0, 'ent_pub_inst_balance_sheet_2013': 0, 'ent_pub_inst_income_stmt_1997': 0, 'ent_pub_inst_income_stmt_2013': 0, 'ent_qualification_record': 0, 'ent_rating_info': 0, 'ent_register_capital': 14, 'ent_repay_li_discount_acc': 0, 'ent_repay_li_guar_acc': 804, 'ent_repay_li_loan_acc': 0, 'ent_report_head': 14, 'ent_reward_record': 0, 'ent_st_repay_liability_sum': 8, 'ent_tax_arrears_record': 0, 'ent_uc_guarantee_sum': 8, 'ent_uc_loan_sum': 14, 'ent_utility_pay_acc': 0, 'ent_utility_pay_detail_in_24m': 0, 'front_mock_xml': 2, 'housing_fund_pay_info': 13056, 'large_amount_instalment_info': 0, 'last_query_record_info': 13056, 'living_info': 65280, 'loan_summary_info': 39168, 'lock_record': 0, 'marriage_info': 13056, 'min_living_security_info': 13056, 'mock_rh_data': 1, 'origin_report_content': 29761, 'other_annotation_info': 0, 'overdue_summary_info': 65280, 'personal_info': 13056, 'phone_info': 65280, 'postpaid_bu_info': 26112, 'postpay_bu_arrears_summary_info': 13056, 'qualification_info': 13056, 'query_record_info': 652800, 'query_record_summary_info': 13056, 'recent_monthly_performance_info': 130560, 'recent_performance_info': 248064, 'recovered_summary_info': 13056, 'repay_detail_in_24_month': 20059544, 'repay_detail_in_5_year': 29683176, 'repay_info_in_24_month': 208896, 'repay_info_in_5_year': 208896, 'repayment_liability_info': 39168, 'repayment_liability_summary_info': 26112, 'report_code_temp': 0, 'report_file_info': 0, 'report_head_other_id': 0, 'report_task_content': 13083, 'report_task_content_copy': 1481, 'report_task_content_copy11': 20, 'report_task_target_field': 29, 'risk_feature_engineering': 0, 'score_info': 0, 'special_event_info': 26112, 'special_trans_info': 39168, 'target_field': 578, 'target_field_conf': 2087, 'target_field_conf_copy1': 2257, 'target_field_conf_new': 0, 'target_file_info': 0, 'tax_arrears_record': 13056}
    # print("原数据数量:" + str(contrastDict))

    # 获取对比数据数量
    # b = ConnMysql.compareTable(basisDict, contrastDict)
    # print("获取对比数据数量:" + str(b))

    # 对比数据数量倍数
    # print("对比数据数量倍数:" + str(ConnMysql.compareResult(b, 100)))

    # 读取contentStr
    # contentStr = ConnMysql.readContent()

    # 读取reportCodeList
    reportCodeList = ConnMysql.readResultCSV()

    for reportCode in reportCodeList:
        # 校验async_task表
        state, execCount = conn.selectAsyncTaskAll(reportCode)
        if conn.selectAsyncTaskCount(reportCode) != 1:
            print("数据量不一致:{}".format(reportCode))
        if state != 1:
            print("async_task表state字段数据不正确:{}".format(reportCode))
        if execCount != 2:
            print("async_task表exec_count字段数据不正确:{}".format(reportCode))
        # 校验origin_report_content表数据长度
        if len(conn.selectContent(reportCode)) != 192135:
            print("origin_report_content表中 {} 数据长度不想等".format(reportCode))
        # 校验origin_report_content表数据
        # if contentStr != conn.selectContent(reportCode):
        #     print("Mysql中 {} 数据不想等".format(reportCode))

    # 指标数TPS
    print("指标数TPS:" + str(conn.targetTPS()))
