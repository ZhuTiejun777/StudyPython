import gitlab
import logging, time
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


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
    def __init__(self):
        self.merge_tag = False
        self.gl = gitlab.Gitlab(url, token)

    def gitlab_merge(self, project_name, merge_tile):
        # 根据id获得project对象
        project = self.gl.projects.get(app_dic[project_name])

        # 创建一个merge request
        try:
            mr = project.mergerequests.create({'source_branch': 'test',
                                               'target_branch': 'master',
                                               'title': merge_tile, })

            # 更新一个merge request 的描述
            mr.description = merge_tile
            mr.save()
            time.sleep(0.2)
            mr.merge()
            time.sleep(0.2)

        except Exception as e:
            logger.error(project_name + "出现错误，错误如下：\n" + str(e))
            self.merge_tag = False
        else:
            logger.info(project_name + "合并成功，合并标题为：" + merge_tile)
            self.merge_tag = True
        # 1表示合并成功，可以后续打tag，0则表示合并失败，后续不打tag
        return self.merge_tag

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

            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)

        # 如果第一次打tag
        else:
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_1.0.01"
            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            logger.info(project_name + "打tag成功" + new_tag_name)


if __name__ == "__main__":
    logger = my_log("gitlab_push")
    url = 'http://192.168.8.79:8081/'
    token = 'fJirgXn1e9GuDk8t-YCn'
    # git工程格式为"app_name":app_dic[project_name]
    app_dic = {
        # 货代
        "bsb-customer":377,
        "bsb-customer-front":376,

    }
    gitlab_handle = gitlab_operation()
    dec_message = str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
        time.localtime().tm_mday) + "日发布"
    for i, j in app_dic.items():
        logger.info("开始处理" + i + str(j) + "项目")
        if gitlab_handle.gitlab_merge(i, dec_message):
            gitlab_handle.gitlab_tag(i, dec_message)
        else:
            logger.info(i + "合并失败，请手动打tag")
