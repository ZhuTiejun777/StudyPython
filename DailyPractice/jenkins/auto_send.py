#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/28 2:09 下午
# @Author :duanming
# @File : send_email.py
import mimetypes
import os
import smtplib
import threading
import time
import schedule
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from os.path import getsize


class EmailManager:
    def __init__(self, **kwargs):
        """
        初始化相关配置信息
        """
        self.kwargs = kwargs
        self.smtp_server = "mail.zjport.gov.cn"
        self.MAX_FILE_SIZE = 10 * 1024 * 1024

    def __get_cfg(self, key, throw=True):
        """
        获取配置参数
        """
        cfg = self.kwargs.get(key)
        if throw == True and (cfg is None or cfg == ""):
            raise Exception("The configuration can't be empty", "utf-8")
        return cfg

    def __init_cfg(self):
        """
        初始化读取到的这些参数信息
        """
        self.msg_from = self.__get_cfg("msg_from")
        self.password = self.__get_cfg("password")
        self.msg_to = ";".join(self.__get_cfg("msg_to"))
        print("init------->", type(self.msg_to))
        # self.msg_cc = ";".join(self.__get_cfg('msg_cc'))
        self.msg_subject = self.__get_cfg("msg_subject")
        self.msg_content = self.__get_cfg("msg_content")
        self.msg_date = self.__get_cfg("msg_date")
        # attachment
        self.attach_file = self.__get_cfg("attach_file", throw=False)

    def login_server(self):
        """
        登录
        """
        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.msg_from, self.password)
        return server

    def get_main_msg(self):
        """
        处理邮件内容
        :return:msg
        """
        msg = MIMEMultipart()
        # message content
        msg.attach(MIMEText(self.msg_content, "plain", "utf-8"))

        msg["From"] = self.msg_from
        msg["To"] = self.msg_to
        print(msg["To"])
        # msg['Cc'] = self._format_addr('To <%s>' % self.msg_cc)
        msg["Subject"] = Header(self.msg_subject, "utf-8")
        msg["Date"] = self.msg_date

        # attachment content
        attach_file = self.get_attach_file()
        if attach_file is not None:
            msg.attach(attach_file)
        return msg

    # def _format_addr(self, *s):
    #     name, addr = parseaddr(s)
    #     return formataddr((Header(name, "utf-8").encode(), addr))

    def get_attach_file(self):
        """
        获取附件的相关信息
        """
        if self.attach_file is not None and self.attach_file != "":
            try:
                if getsize(self.attach_file) > self.MAX_FILE_SIZE:
                    raise Exception(
                        "The attachment is too large and the upload failed!!"
                    )
                with open(self.attach_file, "rb") as file:
                    ctype, encoding = mimetypes.guess_type(self.attach_file, "utf-8")
                    if ctype is None or encoding is not None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)
                    mime = MIMEBase(maintype, subtype)
                    mime.set_payload(file.read())
                    # set header
                    mime.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=os.path.basename(self.attach_file),
                    )
                    mime.add_header("Content-ID", "<0>")
                    mime.add_header("X-Attachment-Id", "0")
                    # set the attachment encoding rules
                    encoders.encode_base64(mime)
                    return mime
            except Exception as e:
                print("%s......" % e)
                return None
        else:
            return None

    def send(self):
        """
        发送邮件
        :return:
        """

        try:
            # initialize the configuration file
            self.__init_cfg()
            # log on to the SMTP server and verify authorization
            server = self.login_server()
            # mail content
            msg = self.get_main_msg()
            # send mail
            server.sendmail(self.msg_from, self.msg_to.split(';'), msg.as_string())
            print("type----->", type(self.msg_to))
            server.quit()
            print("Send succeed!!")
        except smtplib.SMTPException:
            print("Error:Can't send this email!!")

    # 使用python任务定时运行库 schedule 模块
    # def send_mail_by_schedule(manager):
    #     schedule.every(5).minutes.do(manager.send())  # 每5分钟执行一次
    #     # schedule.every().hour.do(manager.send())                   #每小时执行一次
    #     # schedule.every().day.at("23:00").do(manager.send())        #每天23:00执行一次
    #     # schedule.every().monday.do(manager.send())                 #每周星期一执行一次
    #     # schedule.every().wednesday.at("22:15").do(manager.send())  #每周星期三22:15执行一次
    #
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)


if __name__ == "__main__":
    ticks = time.strftime("%Y-%m-%d", time.localtime())
    mail_cfgs = {
        "msg_from": "duanming@zjport.gov.cn",
        "password": "www.521dm.com",
        "msg_to": ["yibao@zjport.gov.cn", "yuanfj@smartebao.com", "1332029758@qq.com"],
        # "msg_cc": ["1332029758@qq.com"],
        "msg_subject": f"易豹bug统计_Date：{ticks}",
        "msg_content": f"Hi,all:\n  易豹 {ticks} 本周低级和修改引入bug统计详情如附件所示，请查收！",
        "attach_file": r"/Users/liuyan/Downloads/缺陷列表 (20200803～20200807).xls",
        "msg_date": time.ctime(),
    }
    manager = EmailManager(**mail_cfgs)
    manager.send()
