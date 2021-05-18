# coding=UTF-8
import re
import sys

chinese_command_compile = re.compile("[\u4e00-\u9fa5]")


def _get_field_len(field):
    field = str(field)
    chinese_count = chinese_command_compile.findall(field)
    return len(field) + 2, len(chinese_count)


def _print_row(row_info, row_len, max_len, file_name=None):
    row_print = []
    for index, len_info in enumerate(max_len):
        row_print.append(sum(len_info) - row_len[index][1])
    if file_name:
        print(("|" + "|".join([str(content).center(row_print[index]) for index, content in enumerate(row_info)]) + "|"),
              file=file_name, flush=True)
        print(("|" + "|".join([str(content).center(row_print[index]) for index, content in enumerate(row_info)]) + "|"),
              file=sys.stdout)
    else:
        print("|" + "|".join([str(content).center(row_print[index]) for index, content in enumerate(row_info)]) + "|")


def print_message(row_infos, field_names=None, result_file=None):
    max_len = []
    # 获取最大总长度
    if field_names:
        title_name_len = [_get_field_len(field_name) for field_name in field_names]
    else:
        title_name_len = []
    max_len.extend(title_name_len)
    title_value_len = []
    for field_infos in row_infos:
        t_field_len = []
        for index, field_info in enumerate(field_infos):
            field_len = _get_field_len(field_info)
            t_field_len.append(field_len)
            if index == len(max_len):
                max_len.append(field_len)
            else:
                # 对比中文数量，最终长度是当前字符串长度+中文字符串之差
                if sum(field_len) > sum(max_len[index]):
                    max_len[index] = field_len
        title_value_len.append(t_field_len)
    # 开始打印头信息
    split_string = "+" + "+".join(["".center(sum(content_len), "-") for content_len in max_len]) + "+"
    if result_file:
        if field_names:
            print(split_string, file=result_file, flush=True)
            print(split_string, file=sys.stdout)
            _print_row(field_names, title_name_len, max_len, result_file)
        print(split_string, file=result_file, flush=True)
        print(split_string, file=sys.stdout)
        # 开始打印数据
        for index, content in enumerate(row_infos):
            _print_row(content, title_value_len[index], max_len, result_file)
        print(split_string, file=result_file, flush=True)
        print(split_string, file=sys.stdout)
        print()
    else:
        if field_names:
            print(split_string)
            _print_row(field_names, title_name_len, max_len, result_file)
        print(split_string)
        # 开始打印数据
        for index, content in enumerate(row_infos):
            _print_row(content, title_value_len[index], max_len, result_file)
        print(split_string)
        print()


def print_table(row_infos, field_names=None):
    from prettytable import PrettyTable
    table = PrettyTable()
    table.field_names = field_names
    for row_info in row_infos:
        table.add_row(row_info)
    print(table)


if __name__ == "__main__":
    title_name = ["node_name", "node_id", "max_time", "min_time", "avg_time", "total_time"]
    data_values = [
        ("内联查询风控初审", "f318532a_ec9cb01a", 1288, 1288, 1288.0, 1288),
        ("查询产品详情", "972c7277", 1238, 1238, 1238.0, 1238),
        ("内联查询风控初审", "d1e83783_ec9cb01a", 1207, 1207, 1207.0, 1207),
        ("调ECIF接口(根据证件信息ECIF查询用户信息", "d56f677b_0b8bd2fa", 1167, 1167, 1167.0, 1167)
    ]

    print_message(data_values, title_name)
    print_table(data_values, title_name)
