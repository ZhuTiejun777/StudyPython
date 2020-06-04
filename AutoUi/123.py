list1 = []
list2 = []
list3 = []

for i in range(1,101):
    # print(i)
    if i % 3 == 0 and i % 5 != 0:
        list1.append(i)
    if i % 3 != 0 and i % 5 == 0:
        list2.append(i)
    if i % 3 == 0 and i % 5 == 0:
        list3.append(i)

print(list1)
print(list2)
print(list3)