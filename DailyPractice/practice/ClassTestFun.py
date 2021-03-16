

class ClassTestFun () :

    done = ["test"]

    def __init__(self):
        self.done = []

    def setup (self) :
        self.done = []
        self.done.append("sss")

    def test02(self):
        self.done = []

    def test01 (self):
        print(self.done)


tt = ClassTestFun()
tt.test02()
tt.setup()
tt.test01()