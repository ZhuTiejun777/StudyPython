class UniqueChars(object):

    def has_unique_chars(self, string):
        num = 0
        for i in range(len(string)):
            print(i)
            for str in string:
                if string[i] == str:
                    num += 1
        print(num,len(string))
        if num == len(string):
            return True
        else:
            return False

uc = UniqueChars()
print(uc.has_unique_chars("qwertyuiopasdfgss"))
