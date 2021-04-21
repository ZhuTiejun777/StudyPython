# 日志模块
import logging
import os
import time
from logging import handlers


class LogGer(object):
    def __init__(self, name):
        os.makedirs("./log") if not os.path.exists("./log") else None  # 创建日志文件文件夹
        get_logger_a = logging.getLogger()
        get_logger_a.setLevel(logging.INFO)  # 设置默认级别
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s[line:%(lineno)d]: %(message)s')
        log_file_path = './log/{}_{}.log'.format(name, time.strftime('%Y%m%d'))
        rotating_handler = handlers.RotatingFileHandler(
            log_file_path, maxBytes=20 * 1024 * 1024, backupCount=10, encoding='utf-8')
        rotating_handler.setFormatter(formatter)
        get_logger_a.addHandler(rotating_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        get_logger_a.addHandler(stream_handler)
        # 过滤级别：控制台输出INFO和WARNING级别，文件只记录WARNING级别
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno < logging.INFO  # 设置过滤等级
        warn_filter = logging.Filter()
        warn_filter.filter = lambda record: record.levelno >= logging.INFO
        # stream_handler.addFilter(info_filter)
        rotating_handler.addFilter(warn_filter)