# Author:jiangnan
# _*_coding:utf-8_*_
# 2020/12/9  11:18
import threading
import time


def func1():
    for i in range(5):
        print('------正在做件事1------')
        time.sleep(1)


def func2():
    for i in range(6):
        print('------正在做件事2------')
        time.sleep(1)


def main():
    # 利用线程执行
    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)
    s_time = time.time()
    t1.start()
    t2.start()
    e_time = time.time()
    print('耗时', e_time - s_time)


# s_time = time.time()
# func1()
# func2()
# e_time = time.time()
# print('耗时', e_time-s_time)
if __name__ == '__main__':
    main()
