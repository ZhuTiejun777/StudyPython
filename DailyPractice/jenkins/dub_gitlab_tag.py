#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: DongYe
# Date: 29/1/2021

import gitlab
import logging, time
from datetime import datetime, timedelta
import logging.handlers
from logging.handlers import TimedRotatingFileHandler


def my_log(log_name):
    '''创建对象的类方法'''
    # 创建日志收集器S
    logger = logging.getLogger(log_name)
    logger.setLevel('DEBUG')
    # 创建日志输出渠道
    sh = logging.StreamHandler()
    sh.setLevel('DEBUG')
    # 按时间进行轮转的收集器
    file_name = datetime.now().strftime("%Y-%m-%d") + ".log"

    fh = TimedRotatingFileHandler(filename=file_name, encoding='utf8', when='D', backupCount=3)
    fh.setLevel('DEBUG')
    # 将日志输出渠道和日志收集器进行绑定
    logger.addHandler(fh)
    logger.addHandler(sh)
    # 设置日志输出格式
    fot = '%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(message)s'
    formatter = logging.Formatter(fot)
    # 将日志输出格式与输出渠道进行绑定
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    return logger


class gitlab_operation(object):

    def __init__(self, tag_name):
        """

        :type tag_name: str 格式：fixbug_yyyymmdd
        """
        self.tag_name = tag_name
        self.gl = gitlab.Gitlab(url, token)

    def have_tag(self, project_name):

        branches = self.gl.projects.get(app_dic[i], all=True).branches.list(all=True)
        branches_list = []
        for baranche in branches:
            branches_list.append(baranche.attributes["name"])
        print("打印所有分支", branches_list)
        if self.tag_name in branches_list:
            return True
        else:
            return False

    def gitlab_tag(self, project_name, tag_description):
        project = self.gl.projects.get(app_dic[project_name])
        tags = project.tags.list()

        # 如果有历史tag
        if tags:

            # 最后一次 tag 名称, 类似于 tag_20200702_1.0.08 格式
            last_tag_name = tags[0].attributes["name"]

            # 提取 1.0.08，打包的时候 version_num 必定有改变
            version_num = last_tag_name[17:19]
            version_two_num = last_tag_name[15]
            version_three_num = last_tag_name[13]

            # 1.0.99中最后两位要进位
            if int(version_num) == 99:

                # 1.9.99 中第二位也要进位
                if int(version_two_num) == 9:
                    new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_" + str(int(version_three_num) + 1) + ".0.00"

                # 只需要进最后两位, version_two_num拼写进去即可，tag_20200702_1.version_two_num.00
                else:
                    new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_" + version_three_num + "." + str(
                        int(version_two_num) + 1) + ".00"

            # 不用进位，最后两位加1。把version_num拼写进去即可。tag_20200702_1.0.version_num
            else:
                new_tag_name = "tag_" + time.strftime(
                    "%Y%m%d") + "_" + version_three_num + "." + version_two_num + "." + "{0:0>2}".format(
                    int(version_num) + 1)

            tag = project.tags.create({'tag_name': new_tag_name, 'ref': self.tag_name})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)

        # 如果第一次打tag
        else:
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_1.0.01"
            tag = project.tags.create({'tag_name': new_tag_name, 'ref': self.tag_name})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)

    def del_tag(self, project_name):
        self.gl.projects.get(app_dic[i], all=True).branches.delete(self.tag_name)
        logger.info(project_name + "成功删除打tag分支\n")


if __name__ == "__main__":
    # git工程格式为"app_name":app_dic[project_name]
    logger = my_log("gitlab_push")
    url = 'http://192.168.8.79:8081/'
    token = 'fJirgXn1e9GuDk8t-YCn'
    dec_message = str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
        time.localtime().tm_mday) + "日发布"
    app_dic = {

        # 前端
        # 这个应用包含 dub-webapp-finance 等
        "dub-front-end-modules": 359,
        "dub-front-end-nb": 89,
        "dub-front-end-sh": 98,
        "dub-front-end-dl": 119,
        "dub-portal-html": 196,
        "dub-front-end": 60,
        "dub-app-inspection": 274,
        "dub-front-datas": 333,
        #
        # 深圳后端
        "dub-import-declare": 68,
        "dub-import-controller": 56,
        "dub-knowledge": 53,
        "dub-finance": 57,
        "dub-custom-receipt": 55,
        "dub-flow": 54,
        "dub-manifest-sz-mutiproject": 181,
        "dub-hezhu-mutiproject": 187,

        # 大连后端
        "dub-dleybsl-multiproject": 193,
        "dub-dlfreight-mutiproject": 194,

        # 公共依赖
        "dub-pojo": 127,
        "dub-common-old": 123,
        "dub-model": 126,
        "dub-common-service": 124,
        "dub-parent": 125,

        # yb 老易豹dub-webapp-index
        "dub-webapps-yb": 128,
        "dub-webapps": 129,
        "dub-manage-webapps": 131,
        "dub-openapi": 132,
        "dub-examine-center": 184,
        "dub-points-mutiproject": 195,

        "dub-dubbo-bill-check": 183,
        "dub-portal-multiproject": 197,
        "dub-szeybsl-multiproject": 179,
        "dub-upload": 192,
        "dub-mobile": 303,

        # exchange 包括dub-exchange-aliyun、dub-exchange-aliyun、dub-xml-exchange、dub-xml-exchange、dub-exchange-eport-sz
        "dub-exchange": 182,
        "dub-exchange-old": 130,
        "dub-web-tools": 198,

        "dub-bill-distribution": 256,
        "dub-customer": 174,
        "dub-export-declare": 122,
        "dub-user": 230,
        "dub-param-controller": 199,
        "dub-baseparam-multiproject": 188,
        "dub-receipt-handler": 309,
        "phx-operate-app": 324,
        "dub-urule": 323,

        # 青岛
        "dub-declare": 299,

        # aeo
        "dub-declare-aeo": 334,

        # 数据埋点
        "dub-track": 369,
    }

    now = datetime.now()
    now = now - timedelta(days=1)
    tag_name = "fixbug_" + now.strftime('%Y%m%d')
    print(tag_name)
    gitlab_handle = gitlab_operation(tag_name)

    for i, j in app_dic.items():
        if gitlab_handle.have_tag(i):
            logger.info("开始处理" + i + str(j) + "项目")
            gitlab_handle.gitlab_tag(i, dec_message)
            gitlab_handle.del_tag(i)
        else:
            print(i + "不需要打tag\n")
