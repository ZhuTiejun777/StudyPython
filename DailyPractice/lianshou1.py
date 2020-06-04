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