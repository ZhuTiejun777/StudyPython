#coding=utf-8
import ddt
import unittest

@ddt.ddt
class DataTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    @ddt.data(
        {"username":"13718369570"},
        {"password":123456}
    )
    @ddt.unpack
    def test_add(self,a):
        print(a)
