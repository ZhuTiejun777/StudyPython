#-*-coding:utf-8-*-
#-*-by zhutj 20200616-*-
from datetime import datetime

from Tools import getagodate, getdatewrite, adddict, getjson, statisticdata, backupsfile, writedata
from data import URL, HEADERS, DATA

# 获取json数据
response_json = getjson(url=URL, headers=HEADERS, data=DATA)
# 创建临时数据
list_temporary = []
sum = 0
# 将历史数据文件备份
backupsfile("testcase", "statisticdata")
for dict_temporary in response_json["rows"]:
    # 将整理的数据写入文件
    writedate = getdatewrite(dict_temporary)
    with open(".//testcase.txt", "a+") as f:
        writedate.continuewrite(f, "标题", "编号", "隶属项目", "提交日期", "提交者", "当前处理人")
        f.write("-" * 50 + "\n")
    # 判断提交时间
    if getagodate(10, dict_temporary["提交日期"]):
        # 添加元素到临时列表
        dicts = adddict(dict_temporary, "编号", "提交日期", "当前处理人")
        list_temporary.append(dicts)
        sum += 1
f.close()
print("新问题总数量为:" + str(sum))
list_statistic = statisticdata(list_temporary)
# 将统计数据写入文件
writedata("statisticdata", list_statistic)









