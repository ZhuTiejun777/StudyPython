import logging
import os
import time
from logging import handlers

import pymysql


class LogGer(object):
    def __init__(self, name):
        os.makedirs("../log") if not os.path.exists("../log") else None  # 创建日志文件文件夹
        get_logger_a = logging.getLogger()
        get_logger_a.setLevel(logging.INFO)  # 设置默认级别
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d]: %(message)s')
        log_file_path = './log/{}_{}.log'.format(name, time.strftime('%Y%m%d'))
        rotating_handler = handlers.RotatingFileHandler(log_file_path, maxBytes=20 * 1024 * 1024, backupCount=10, encoding='utf-8')
        rotating_handler.setFormatter(formatter)
        get_logger_a.addHandler(rotating_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        get_logger_a.addHandler(stream_handler)
        # 过滤级别：控制台输出INFO和WARNING级别，文件只记录WARNING级别
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno < logging.WARNING  # 设置过滤等级
        warn_filter = logging.Filter()
        warn_filter.filter = lambda record: record.levelno >= logging.WARNING
        # stream_handler.addFilter(info_filter)
        rotating_handler.addFilter(warn_filter)




class MedicalSpider:
    LogGer(str(os.path.basename(__file__))[:-3])

    def __init__(self):
        logging.info('system is working now.')
        # 有更改
        self.database = "msd"  # 医疗爬虫数据库名
        self.table_hospital = "medical_spider_hospital"  # 医院表名
        self.table_doctor = "medical_spider_doctor"  # 医生表名
        self.mysql_config = {
            'host': '192.168.3.238', "user": 'syd', "passwd": 'Syd0523', 'db': self.database, "autocommit": True
        }
        self.db = pymysql.Connect(**self.mysql_config)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        self.base_info = {
            '所属省份': "上海市",
            '所属城市': "上海市",
            '所属区县': None,
            '医院标识': "06d00a62b09dccb2",
            '医院名称': "复旦大学附属金山医院",
            '医院官网': "www.jinshanhos.org.cn",
        }

    def __insert(self, table, item):
        try:
            self.cursor.execute("insert into %s(%s) values(%s)" % (
                table,
                ",".join('`{}`'.format(k) for k in item.keys()),
                ','.join('%({})s'.format(k) for k in item.keys())
            ), item)
            return logging.info('save success:{}'.format(item)), 1
        except Exception as e:
            return logging.warning('save failed:{},item:{}'.format(item, e)), 0

    def insert(self, table, items):
        """
        :param table: 数据表名
        :param items: 传入字典或者"[字典]" 字典中的“键”必须包含在“表字段”，“表字段”多余或等于字典的“键”
        :return: 返回插入成功的行数
        """
        items = items if isinstance(items, list) else [items]
        return sum([a for (_, a) in [self.__insert(table, item) for item in items] if a])


if __name__ == '__main__':
    print("test")