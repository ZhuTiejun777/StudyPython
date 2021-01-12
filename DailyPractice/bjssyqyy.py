# -*- coding: utf-8 -*-
# ☯ Author: ChinaPython
# ☯ Email : chinapython@yeah.net
# ☯ Date  : 2020/12/27 20:13
import os
import time
import random
import logging
import pymysql
import requests
from lxml import etree
from logging import handlers


# 日志模块
class LogGer(object):
    def __init__(self, name):
        os.makedirs("../log") if not os.path.exists("../log") else None  # 创建日志文件文件夹
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
        info_filter.filter = lambda record: record.levelno < logging.WARNING  # 设置过滤等级
        warn_filter = logging.Filter()
        warn_filter.filter = lambda record: record.levelno >= logging.WARNING
        # stream_handler.addFilter(info_filter)
        rotating_handler.addFilter(warn_filter)


# 爬虫主程序
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

    @staticmethod
    def random_ua():
        return "Mozilla/5.0 (Windows NT {}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{} Safari/537.36".format(
            random.choice([
                '10.0; Win64; x64', '10.0; WOW64', '10.0',
                '6.2; WOW64', '6.2; Win64; x64', '6.2',
                '6.1', '6.1; Win64; x64', '6.1; WOW64'
            ]), random.choice([
                '70.0.3538.16', '70.0.3538.67', '70.0.3538.97', '71.0.3578.137', '71.0.3578.30', '71.0.3578.33',
                '71.0.3578.80', '72.0.3626.69', '72.0.3626.7', '73.0.3683.20', '73.0.3683.68', '74.0.3729.6',
                '75.0.3770.140', '75.0.3770.8', '75.0.3770.90', '76.0.3809.12', '76.0.3809.126', '76.0.3809.25',
                '76.0.3809.68', '77.0.3865.10', '77.0.3865.40', '78.0.3904.105', '78.0.3904.11', '78.0.3904.70',
                '79.0.3945.16', '79.0.3945.36', '80.0.3987.106', '80.0.3987.16', '81.0.4044.138', '81.0.4044.20',
                '81.0.4044.69', '83.0.4103.14', '83.0.4103.39', '84.0.4147.30', '85.0.4183.38', '85.0.4183.83',
                '85.0.4183.87', '86.0.4240.22', '87.0.4280.20', '87.0.4280.88', '88.0.4324.27'
            ]))

    def requester(self, url, retry=3, **kwargs):
        """
        :param url: 必须传入的url
        :param retry: 不需要自己传，自动忽视
        :param kwargs: 传递需要的参数，必须“参数名=参数”
        :return: 返回正常访问的内容或者返回None
        """

        try:
            return requests.request(
                url=url,
                method=kwargs.get('method') if kwargs.get('method') else 'get',
                timeout=kwargs.get('timeout') if kwargs.get('timeout') else 30,
                params=kwargs.get('params'),
                data=kwargs.get('data'),
                files=kwargs.get('files'),
                json=kwargs.get('json'),
                cookies=kwargs.get('cookies'),
                allow_redirects=True if kwargs.get('allow_redirects') in [None, True] else False,
                proxies={
                    'http': 'http://{}'.format(kwargs.get('proxies')),
                    'https': 'https://{}'.format(kwargs.get('proxies'))
                } if kwargs.get('proxies') else None,
                headers=kwargs.get('headers') if kwargs.get('headers') else {
                    'Accept': '*/*',
                    'Connection': 'close',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'User-Agent': self.random_ua()
                },
                verify=False
            )
        except Exception as e:
            return logging.warning('request error:%s' % e) if retry < 1 else self.requester(url, retry - 1, **kwargs)

    """
    可加入站点采集函数  例如:列表页--详情页
    """

    # 采集医院信息
    def get_hospital(self):
        response = self.requester(url='http://www.hospitalshy.com/Hospitals/Main/Description')
        if response is None:
            return logging.warning('获取简介失败...')
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        content = '\n'.join([t for t in html.xpath('//div[@class="article_cont"]/p/text()') if len(t.strip()) > 0])
        return dict(self.base_info, **{
            '医院电话': "010-69423220",
            '医院邮箱': "syyybgs@163.com",
            '医院等级': "三级",
            '医院地址': "北京市顺义区光明南街3号",
            '医院简介': content,
            '采集链接': "http://www.hospitalshy.com/Hospitals/Main/Description",
            '采集时间': time.strftime('%Y-%m-%d'),
        })

    def get_doctor(self):
        response = self.requester(url='http://www.hospitalshy.com/Html/Hospitals/Doctors/Overview0.html')
        if response is None:
            return logging.warning('获取医生列表失败...')
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        tasks = list()
        for temp in html.xpath('//ul[@class="menuB"]/div[contains(@class,"menuCount")]/h2[@class="DepName"]'):
            depart = ''.join(temp.xpath('./a/text()')).strip()
            for t in temp.xpath('./following-sibling::ul/li/a'):
                tasks.append({
                    '所属科室': depart,
                    '医生名称': ''.join(t.xpath('./text()')).strip(),
                    '采集链接': 'http://www.hospitalshy.com' + ''.join(t.xpath('./@href')).strip(),
                    '采集时间': time.strftime('%Y-%m-%d')
                })
        for task in tasks:
            time.sleep(random.uniform(1, 3))
            # print(task)
            response = self.requester(task['采集链接'])
            if response is None:
                continue
            response.encoding = response.apparent_encoding
            html = etree.HTML(response.text)
            item = dict(task, **{
                '医生级别': ''.join(html.xpath('//div[@class="doct_con"]/p[1]/text()')).strip(),
                '医生职务': ''.join(html.xpath('//div[@class="doct_con"]/p[contains(text(),"职务：")]/text()')).strip(),
                '医生图片': 'http://www.hospitalshy.com' + ''.join(html.xpath('//a[@class="doct_img"]/img/@src')).strip(),
                '医生技能': ''.join([i.strip() for i in html.xpath(
                    '//div[@class="doct_con"]/p[contains(text(),"擅长：")]//text()') if len(i.strip()) > 0]).strip(),
                '医生简介': ''.join(
                    html.xpath('//div[@class="Department_left"]/div[@class="tab mb20"]/div[1]/p/text()')).strip()
            })
            item['医生职务'] = None if len(item['医生职务']) == 0 else item['医生职务'].replace('职务：', '')
            item['医生图片'] = None if 'doct.jpg' in item['医生图片'] else item['医生图片']
            item['医生技能'] = None if len(item['医生技能']) == 0 else item['医生技能'].replace('擅长：', '')
            item['医生简介'] = None if len(item['医生简介']) == 0 else item['医生名称'] + ' ' + item['医生简介']
            self.insert(self.table_doctor, item)
            # break

    # 运行入口
    def run(self):
        """
        加入采集逻辑,最终必须关闭 数据库“游标”，“连接”
        """
        hospital_info = self.get_hospital()
        if hospital_info is None:
            return
        self.insert(self.table_hospital, hospital_info)
        self.get_doctor()
        self.cursor.close(), self.db.close()


if __name__ == '__main__':
    start = MedicalSpider()
    start.run()
