list = [1, 2, 3, 4, 5]

newlist = [1 / x if x != 0 else 0 for x in list]

print(newlist)