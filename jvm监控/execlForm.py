import os
import re

import xlwt


def txtXls(filename, xlsname):
    try:
        f = open(filename)
        xls = xlwt.Workbook()
        # 生成excel的方法，声明excel
        sheet = xls.add_sheet('sheet', cell_overwrite_ok=True)
        x = 0  # 在excel开始写的位置（y）
        while True:  # 循环读取文本里面的内容
            line = f.readline()  # 一行一行的读
            stripLine = line.strip()
            reLine = re.sub(" +", "\t", stripLine)
            if not line:  # 如果没有内容，则退出循环
                break
            if x == 0:
                x += 1
                continue
            print(reLine.split('\t'))
            for i in range(len(reLine.split('\t'))):  # \t即tab健分隔
                item = reLine.split('\t')[i]
                sheet.write(x, i, item)  # x单元格经度，i单元格纬度
            x += 1  # 另起一行
        f.close()
        xls.save(xlsname)  # 保存为xls文件
    except:
        raise


filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "execl/gc-2021-05-17-2.log")
xlsPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "execl/test.xlsx")

txtXls(filePath, xlsPath)