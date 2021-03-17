import time

import gitlab


class A():
    def a(self):
        print("a")

class B():
    def b(self):
        print("b")

class C():
    def c(self):
        print("c")

class D(A, B, C):
    pass

d = D()
d.a()
d.b()
d.c()



gl = gitlab.Gitlab("http://192.168.8.79:8081/", "P8JVoExKCn8-oydS8sRz")

dictProjects = {}
print(gl.projects.list(all=True))
for p in gl.projects.list(all=True, as_list=False):
    print(p.name, p.id)
    dictProjects[p.name] = p.id

print(dictProjects)

print(gl.projects.get(dictProjects.get("kwe")))

print(gl.projects.get(dictProjects.get("kwe")).tags.list())

print(str(time.localtime().tm_year) + "年" + str(time.localtime().tm_mon) + "月" + str(
    time.localtime().tm_mday) + "日发布")
