# 项目根目录常量
import os
import logging.handlers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))


# 初始化日志配置

def init_log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    lgs = logging.StreamHandler()
    log_path = BASE_DIR + "/log/tpshop.log"
    lgh = logging.handlers.TimedRotatingFileHandler(log_path, when="midnight", interval=1
                                                    , backupCount=5, encoding="utf-8")

    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s")

    lgs.setFormatter(fmt)
    lgh.setFormatter(fmt)

    logger.addHandler(lgs)
    logger.addHandler(lgh)
