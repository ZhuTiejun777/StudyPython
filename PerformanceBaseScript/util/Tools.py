# -*- coding: UTF-8 -*-
__Author__ = "zhutiejun777"
__Date__ = "2021/04/11"

import datetime
import logging
import os
import random

from LogGer import LogGer

LogGer(str(os.path.basename(__file__))[:-3])


def randomLengthInt(length: int = 10):
    intStr = ""
    if length > 64:
        logging.info("字符长度不可大于64!")
        length = 64
    number = length
    while length:
        if length == number:
            intStr += str(random.randint(1, 9))
        else:
            intStr += str(random.randint(0, 9))
        length -= 1
    return intStr


def randomChinese(count: int = 10):
    import random
    str = ""
    if count < 0 or count > 100:
        logging.info("输入大于0，小于100的数字")
        count = 10
    while count:
        str += chr(random.randint(0x4e00, 0x9fbf))
        count -= 1
    return str


def randomEnglish(count: int = 18):
    import random
    strRes = ""
    if count < 0 or count > 64:
        logging.info("输入大于0，小于64的数字")
        count = 18
    while count:
        strRes += chr(random.randint(97, 122))
        count -= 1
    return strRes

def randomEnglishInt(count: int = 10):
    import random
    strRes = ""
    if count < 0 or count > 100:
        logging.info("输入大于0，小于100的数字")
        count = 10
    while count:
        parameter = random.randint(0, 1)
        if parameter == 0:
            strRes += chr(random.randint(97, 122))
            # strRes += chr(random.randint(97, 122))
        if parameter == 1:
            strRes += str(random.randint(0, 9))
        count -= 1
    return strRes

def getId_no():
    """
    getId_no:随机生成身份证号
    """
    str1_6=['370982', '371402', '370781', '370983', '371581', '370100', '371302', '371122', '370304', '370402', '370404', '371325', '370303', '370000', '371000', '370305', '370214', '370302', '370828', '371326', '370322', '370900', '370611', '371423', '371524', '371424', '371328', '370784', '370811', '371728', '370181', '370124', '370321', '371121', '370826', '370704', '370212', '370503', '371521', '370523', '370285', '370281', '371603', '371721', '370300', '371600', '370902', '370681', '370282', '371724', '370521', '371400', '371422', '371323', '371723', '370921', '370602', '370600', '370830', '370684', '370700', '371103', '370883', '370306', '370634', '371502', '370103', '371481', '371329', '371621', '371482', '370686', '370832', '370812', '370202', '370911', '371200', '371327', '371312', '370683', '371403', '371622', '370923', '371722', '370481', '370104', '371522', '370403', '370112', '371526', '371083', '371425', '370211', '371300', '370702', '371626', '370829', '370406', '371428', '370500', '370105', '370802', '370827', '371700', '371525', '371623', '370831', '371602', '370785', '371082', '370102', '370125', '371322', '371427', '370786', '370705', '371727', '370687', '370725', '370200', '370800', '371725', '371100', '370612', '371625', '370613', '370502', '370685', '371426', '370782', '371002', '371311', '370703', '371102', '371202', '370405', '371500', '370400', '370881', '371726', '370522', '370203', '371203', '370682', '370283', '371324', '371702', '370783', '371523', '370213', '370113', '371321', '370126', '370724', '370323', '371081']
    str7_9=["195","196","197","198","199"]
    coefficientArray = [ "7","9","10","5","8","4","2","1","6","3","7","9","10","5","8","4","2"]# 加权因子
    MapArray=["1","0","X","9","8","7","6","5","4","3","2"]
    str10=str(random.randint(1, 9))
    str11_12 = str(random.randint(1, 12)).zfill(2)
    str13_14 = str(random.randint(1, 27)).zfill(2)
    str15_17 = str(random.randint(1, 999)).zfill(3)
    m = random.randint(0, len(str1_6)-1)
    n = random.randint(0, len(str7_9)-1)
    tempStr=str1_6[m]+str7_9[n]+str10+str11_12+str13_14+str15_17
    total = 0
    for i in range(len(tempStr)):
        total = total + int(tempStr[i])*int(coefficientArray[i])
    parityBit=MapArray[total%11]
    ResultIDCard=tempStr+parityBit
    return ResultIDCard


def getName():
    """
    getName:随机生成姓名
    """
    import random as r
    surname = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
            '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
            '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
            '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
            '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
            '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
            '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫', '万俟', '闻人',
            '夏侯', '诸葛', '尉迟', '公羊', '赫连', '澹台', '皇甫', '宗政', '濮阳', '公冶', '太叔', '申屠', '公孙', '慕容', '仲孙', '钟离',
            '长孙', '宇文', '司徒', '鲜于', '司空', '闾丘', '子车', '亓官', '司寇', '巫马', '公西', '颛孙', '壤驷', '公良', '漆雕', '乐正']

    namenum=r.choice([1,2])
    if namenum == 1:
        #name=r.choice(surname)+chr(r.randint(19968,40896))
        name=r.choice(surname)+chr(r.randint(19968,21000))
    else :
        #name=r.choice(surname)+chr(r.randint(19968,40896))+chr(r.randint(19968,40896))
        name=r.choice(surname)+chr(r.randint(19968,21000))+chr(r.randint(19968,21000))
    return name

def getMoble():
    """
    getMoble:随机生成手机号码
    """
    prefixArray = ("130", "131", "132", "133", "135", "137", "138", "170", "187", "189")
    i = random.randint(0, len(prefixArray)-1)
    prefix = prefixArray[i]
    telnum=createSerial(8)
    return prefix+telnum

def createSerial(numbercount:int=0):
    from datetime import datetime
    Serial=str(datetime.now().strftime('%Y%m%d%H%M%S%f'))
    numbercount=int(numbercount)
    if numbercount==0:
        return Serial
    else:
        if numbercount>0 and numbercount<21:
            Serial=Serial[-numbercount:]
            return Serial
        elif numbercount>20:
            numelsecout=numbercount-20
            numelse=str(random.randint(int('1'+'0'*(numelsecout-1)), int('9'*numelsecout)))
            return numelse+Serial
        else:
            print('createSerial的参数值必须大于0，请检查！')
            # raise CollectUtilError('createSerial的参数值必须大于0，请检查！')

def getDate():
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
