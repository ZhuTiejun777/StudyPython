# coding = utf-8
import random
import support.globalVars as globalVars
import re
import datetime
import threading

systemRandom = random.SystemRandom()
lock = None
manager = {}
r_lock = threading.Lock()
ex_email = re.compile(r'^[\w][a-zA-Z1-9.]{4,19}@[a-zA-Z0-9]+.(com|gov|net)$')
ex_num = re.compile(r'^[\w][a-zA-Z1-9.]{4,19}@[a-zA-Z0-9]+.(com|gov|net)$')
email_ext = "@yunrong.cn"


def create_random_chinese(chinese_len: int = 3):
    """
    create_random_chinese：创建指定长度随机中文的字符串
    chinese_len：随机字符串长度,默认长度为3
    """
    return "".join([chr(systemRandom.randint(19968, 40869)) for _ in range(int(chinese_len))])


def create_random_string(string_len: int = 10):
    """
    create_random_string：创建指定长度随机数字和字母的字符串
    string_len：随机字符串长度,默认长度为10
    """
    random_string = ""
    for _ in range(int(string_len)):
        tmp_int = systemRandom.randrange(1, 63)
        if tmp_int < 11:
            tmp_int += 47
        elif tmp_int < 37:
            tmp_int += 54
        else:
            tmp_int += 60
        random_string += chr(tmp_int)
    return random_string


def get_id_no():
    """
    get_id_no:随机生成身份证号
    """
    # 年
    str7_10 = str(systemRandom.randint(1950, 2019))
    # 月
    str11_12 = str(systemRandom.randint(1, 12)).zfill(2)
    # 日
    str13_14 = str(systemRandom.randint(1, 27)).zfill(2)
    # 顺序号
    str15_17 = str(systemRandom.randint(1, 999)).zfill(3)
    m = systemRandom.randint(0, globalVars.area_dict_codes_len-1)
    temp_str = globalVars.area_dict_codes[m]+str7_10+str11_12+str13_14+str15_17
    total = 0
    for i in range(len(temp_str)):
        total = total + int(temp_str[i])*int(globalVars.coefficient_array[i])
    return temp_str+globalVars.map_array[total % 11]


def create_random_num(number_len: int = 10):
    """
    create_random_num:生成指定长度的数字字符串
    """
    return "".join([str(systemRandom.randint(0, 9)) for _ in range(int(number_len))])


def get_mobile():
    """
    getMoble:随机生成手机号码
    """
    return globalVars.mobile_array[systemRandom.randint(0, globalVars.mobile_array_len-1)] + create_random_num(8)


def get_bankcard():
    """
    get_bankcard:随机获得银行卡号
    """
    card_bin, card_len = random.choice(list(globalVars.card_bin.items()))
    return card_bin + create_random_num(int(card_len)-len(card_bin))


def increase(column_name, start_num):
    global manager
    with lock:
        data = manager["data"]
        data[column_name] = data.get(column_name, int(start_num)) + 1
        manager["data"] = data
        return str(data[column_name])


def get_email(email_len):
    email_len = int(email_len)
    if email_len < len(email_ext):
        raise RuntimeError("邮件长度字段小于最低长度要求")
    return create_random_string(email_len - len(email_ext)) + email_ext


# 字符和函数的映射关系，如果有新的字符需要在这里添加，否则将不做处理
f_s_m = {
    "S": create_random_string,
    "N": create_random_num,
    "C": get_id_no,
    "M": get_mobile,
    "CH": create_random_chinese,
    "I": increase,
    "B": get_bankcard,
    "E": get_email
}
chinese_pattern = r'[\u4e00-\u9fa5]+'


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 定义默认书写规则
def suggest(column_value: str, max_length=None, is_increase=False):
    value_length = len(column_value)
    # 以当前值的长度为优先
    max_length = value_length or max_length
    if re.match(chinese_pattern, column_value):
        # 判断是否全为中文
        return "${"+"CH-{}".format(max_length)+"}"
    elif _is_number(column_value):
        # 如果为全为数字，判断是否为自增主键
        if is_increase:
            return "${" + "I-{}".format(int(column_value)+1) + "}"
        else:
            # 判断是否为手机号
            # 获取前3位
            str_0_2 = column_value[:3]
            if str_0_2 in globalVars.mobile_array and value_length == 11:
                # 如果前3位在手机号段数组中，且总位数是11位，且判断为手机号
                return "${M}"
            elif column_value[:6] in globalVars.card_bins and str(len(column_value)) == globalVars.card_bin.get(column_value[:6]):
                # 判断是不是银行卡
                return "${B}"
            else:
                # 判断是不是身份证
                str_0_5 = column_value[:6]
                str_6_14 = column_value[6:14]
                if str_0_5 in globalVars.area_dict_codes:
                    # 如果区域码和出生年月都匹配前面14位，且初步判断是身份证
                    try:
                        datetime.datetime.strptime(str_6_14, '%Y%m%d')
                        return "${C}"
                    except ValueError:
                        pass
                return "${"+"N-{}".format(max_length)+"}"
    else:
        # 如果不是纯数字，进一步做判断
        if ex_email.match(column_value):
            # 如果为邮箱则创建
            return "${" + "E-{}".format(max_length) + "}"
        else:
            return "${" + "S-{}".format(max_length) + "}"


if __name__ == "__main__":
    list = []
    for key in globalVars.area_dict:
        if key[0: 2] == "37":
            list.append(key)
    print(list)