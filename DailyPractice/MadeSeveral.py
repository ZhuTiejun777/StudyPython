def randomChinese(count:int=10):
    import random
    str = ""
    if count < 0 or count > 32:
        print("输入大于0，小于32的数字")
        count = 10
    while count:
        str += chr(random.randint(0x4e00, 0x9fbf))
        count -= 1
    return str

def randomEnglish(count:int=18):
    import random
    str = ""
    if count < 0 or count > 64:
        print("输入大于0，小于64的数字")
        count = 18
    while count:
        str += chr(random.randint(97, 122))
        count -= 1
    return str

def randomLengthInt(length:int=10):
    import random
    intStr = ""
    if length > 64:
        print("字符长度不可大于64!")
        length = 64
    number = length
    while length:
        if length == number:
            intStr += str(random.randint(1, 9))
        else:
            intStr += str(random.randint(0, 9))
        length -= 1
    return intStr


