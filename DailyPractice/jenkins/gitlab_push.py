import gitlab, time
#from dub_script.logging_manage import my_log

#logger = my_log("gitlab_push")
print("gitlab_push")
url = 'http://192.168.8.79:8081/'
# token = 'fJirgXn1e9GuDk8t-YCn'
token = 'QtRTnbBJyf1nZxbpM111'

# 登录
gl = gitlab.Gitlab(url, token)

dec_message = str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
    time.localtime().tm_mday) + "日发布"


class gitlab_operation(object):
    def __init__(self):
        self.merge_tag = False

    def gitlab_merge(self, project_name, merge_tile):
        # 根据id获得project对象
        project = gl.projects.get(app_dic[project_name])

        # 创建一个merge request
        try:
            mr = project.mergerequests.create({'source_branch': 'test',
                                               'target_branch': 'master',
                                               'title': merge_tile, })

            # 更新一个merge request 的描述
            mr.description = merge_tile
            mr.save()
            mr.merge()
        except Exception as e:
            #logger.error(project_name + "出现错误，错误如下：\n" + str(e))
            print(project_name + "出现错误，错误如下：\n" + str(e))
            self.merge_tag = False
        else:
            #logger.info(project_name + "合并成功，合并标题为：" + merge_tile)
            print(project_name + "合并成功，合并标题为：" + merge_tile)
            self.merge_tag = True
        # 1表示合并成功，可以后续打tag，0则表示合并失败，后续不打tag
        return self.merge_tag

    def gitlab_tag(self, project_name, tag_description):
        project = gl.projects.get(app_dic[project_name])
        tags = project.tags.list()

        # 如果有历史tag
        if tags:
            last_tag_name = tags[0].attributes["name"]

            # 最后需要加1
            version_num = int(last_tag_name[18:20]) + 1
            # 拼接，满足 tag_20200702_V2.0.08 格式
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_V2.0." + "{0:0>2}".format(version_num)
            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            #logger.info(project_name + "打tag成功" + new_tag_name)
            print(project_name + "打tag成功" + new_tag_name)

        # 如果第一次打tag
        else:
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_V2.0.01"
            tag = project.tags.create({'tag_name': new_tag_name, 'ref': 'master'})
            tag.set_release_description(tag_description)
            #logger.info(project_name + "打tag成功" + new_tag_name)
            print(project_name + "打tag成功" + new_tag_name)

if __name__ == "__main__":
    # git工程格式为"app_name":app_dic[project_name]
    app_dic = {
        "tsn-webapp-ui": 251,       # 易豹货代前端VUE
        # "tsn-analysis": 211,        # 统一分析查询应用
        # "tsn-inspection": 208,      # 商检待办应用模块
        # "tsn-report": 170,          # 报表应用
        # "tsn-finance": 168,         # 财务模块应用
        # "tsn-uct": 167,             # 基础用户、客户类信息维护应用
        "tsn-shipping-export": 165,  # 海运出口业务应用
        # "tsn-fee": 161,             # 费用业务应用
        # "tsn-air-export": 145,      # 空运出口
        # "tsn-air-import": 144,      # 空运进口
        # "tsn-exchange": 136,        # 交换应用
        # "tsn-shipping-import": 135,  # 海运进口
        # "tsn-base": 67,             # 基础参数、基础服务应用工程
        # "tsn-common": 137,            # 基础组件
        # "bsb-doc": 273              # 单证服务
    }
    gitlab_handle = gitlab_operation()
    for i, j in app_dic.items():
        #logger.info("开始处理" + i + str(j) + "项目")
        print("开始处理" + i + str(j) + "项目")
        if gitlab_handle.gitlab_merge(i, dec_message):
            gitlab_handle.gitlab_tag(i, dec_message)
        else:
            #logger.info(i + "合并失败，请手动打tag")
            print(i + "合并失败，请手动打tag")