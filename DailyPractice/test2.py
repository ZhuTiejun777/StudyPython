import time
import unittest

import gitlab


class test2(unittest.TestCase):

    def test01(self):
        gl = gitlab.Gitlab("http://192.168.8.79:8081/", "P8JVoExKCn8-oydS8sRz")
        dictProjects = {}
        print(gl.projects.list(all=True))
        for p in gl.projects.list(all=True, as_list=False):
            print(p.name, p.id)
            dictProjects[p.name] = p.id
        print(dictProjects)
        print(gl.projects.get(dictProjects.get("kwe")))
        print("-" * 50)
        print(gl.projects.get(dictProjects.get("kwe")).tags.list()[0].attributes["name"])

    def test02(self):
        print(str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
            time.localtime().tm_mday) + "日发布")

    def test03(self):
        str = "tag_20210222_v1.0.32"
        print(str[-2:])
        print("{0:0>2}".format(str[-2:]))

    def test04(self):
        gl = gitlab.Gitlab("http://192.168.8.79:8081/", "P8JVoExKCn8-oydS8sRz")
        dictProjects = {}
        #print(gl.projects.list(all=True))
        for p in gl.projects.list(all=True, as_list=False):
            print(p.name, p.id)
            dictProjects[p.name] = p.id
        #project = gl.projects.get(dictProjects.get("kwe"))
        project = dictProjects.get("ssssss")
        print(project)


