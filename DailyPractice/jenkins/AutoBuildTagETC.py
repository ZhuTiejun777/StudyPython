import sys

import gitlab, time

url = 'http://192.168.8.79:8081/'
token = 'P8JVoExKCn8-oydS8sRz'

dec_message = str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
    time.localtime().tm_mday) + "日发布"

list = ["kwl","kwe"]
workspacePath=sys.argv[1]

class gitlab_operation(object):
    def __init__(self):
        self.merge_tag = False
        self.gl = gitlab.Gitlab(url, token)
        self.dictProjects = {}
        for p in self.gl.projects.list(all=True, as_list=False):
            self.dictProjects[p.name] = p.id

    def gitlab_merge(self, project_name, merge_tile):

        # TODO 增加为空判断
        if self.dictProjects.get(project_name) == None:
            self.merge_tag = False
            return self.merge_tag
        # 根据id获得project对象
        project = self.gl.projects.get(self.dictProjects.get(project_name))

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
        project = self.gl.projects.get(self.dictProjects.get(project_name))
        tags = project.tags.list()

        # 如果有历史tag
        if tags:
            #attributes获取属性
            last_tag_name = tags[0].attributes["name"]

            # 最后需要加1
            version_num = int(last_tag_name[-2:]) + 1
            # 拼接，满足 tag_20210222_v1.0.32 格式
            new_tag_name = "tag_" + time.strftime("%Y%m%d") + "_v1.0." + "{0:0>2}".format(version_num)
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

    gitlab_handle = gitlab_operation()
    for i in list:
        #logger.info("开始处理" + i + str(j) + "项目")
        print("开始处理" + i + "项目")
        if gitlab_handle.gitlab_merge(i, dec_message):
            gitlab_handle.gitlab_tag(i, dec_message)
        else:
            #logger.info(i + "合并失败，请手动打tag")
            print(i + "合并失败，请手动打tag")