item = "item"
hash = 1234
for i in range(4):
    print("------ i = ", i, " --------")
    for x in item:
        # hash = ord(x) << 5 + 2 ** i + hash / 4
        hash = (ord(x) << 5) + 2 ** (i + 4) + hash
        print(hash)
# print(((item << 2) + item / 5) * 2 + 2 % 2)



# hash = 5381
#         for x in s:
#             hash = ((hash << 5) + hash) + ord(x)