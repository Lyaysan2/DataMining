import csv

support = 4

product_code = {}  # {'PRD00':0, 'PRD01':1, ...}
item_count = {}
transaction_list = {}
doubletons = {}
hash_bucket1 = []
hash_bucket2 = []
doubleton_code = {}

with open('/Users/lyaysanz/Desktop/transactions.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    header = next(csv_reader)

    code_numb = 0
    for row in csv_reader:
        # create a mapping table for string product names with their numeric code
        # for each product we count the number of its occurrences
        if row[0] in product_code.keys():
            item_count[product_code[row[0]]] += 1
        else:
            product_code[row[0]] = code_numb
            item_count[code_numb] = 1
            code_numb += 1

        # distribute products according to their transactions
        if row[1] in transaction_list.keys():
            transaction_list[row[1]].append(product_code[row[0]])
        else:
            transaction_list[row[1]] = []
            transaction_list[row[1]].append(product_code[row[0]])

print("product_code")
# print(product_code)

print("trans_list")
# print(transaction_list)

# list for deleted item
deleted_item = []

print("item count")
# print(item_count)

# remove from items everything that does not satisfy the level of support
for item in list(item_count.keys()):
    if item_count[item] < support:
        deleted_item.append(item)
        item_count.pop(item)

print("deleted_item")
# print(deleted_item)

# make groups of doubletons
for tran in transaction_list.keys():
    for prod in transaction_list[tran]:
        doubletons[tran] = []
    for i in range(len(transaction_list[tran]) - 1):
        for j in range(i, len(transaction_list[tran])):
            if i != j:
                doubletons[tran].append([transaction_list[tran][i], transaction_list[tran][j]])

print("transaction list pare")
# print(doubletons)

# for each doubleton we create a code
k = 0
for i in doubletons.values():
    for j in range(len(i)):
        if i[j] not in doubleton_code.values():
            doubleton_code[k] = i[j]
            k += 1

print("doubleton code")
# print(doubleton_code)

# initialize hash buckets
for i in range(len(product_code)):
    hash_bucket1.append([])
    hash_bucket1[i] = {}

    hash_bucket2.append([])
    hash_bucket2[i] = {}

# fill in the first hash bucket
for i in doubletons.values():
    for j in range(len(i)):
        mod = (int(i[j][0]) + int(i[j][1])) % len(product_code)
        for k, v in doubleton_code.items():
            if v == i[j]:
                if hash_bucket1[mod].get(k) is not None:
                    hash_bucket1[mod][k] += 1
                else:
                    hash_bucket1[mod][k] = 1

# fill in the second hash bucket
for i in doubletons.values():
    for j in range(len(i)):
        mod = (int(i[j][0]) + 2 * int(i[j][1])) % len(product_code)
        for k, v in doubleton_code.items():
            if v == i[j]:
                if hash_bucket2[mod].get(k) is not None:
                    hash_bucket2[mod][k] += 1
                else:
                    hash_bucket2[mod][k] = 1

# list for deleted doubletons
deleted_pare_code = []

# look at the support level
for i in hash_bucket1:
    if sum(i.values()) < support:
        for code in i.keys():
            deleted_pare_code.append(code)
            doubleton_code.pop(code)

for i in hash_bucket2:
    # remove the doubletons that are removed in hash_bucket1
    for j in list(i.keys()):
        if j in deleted_pare_code:
            i.pop(j)
    if sum(i.values()) < support:
        for code in i.keys():
            doubleton_code.pop(code)

print("hash basket1")
# print(hash_bucket1)

print("hash basket2")
# print(hash_bucket2)

# delete doubletons which contains not frequent items
for code, pair in list(doubleton_code.items()):
    for item in pair:
        if item in deleted_item:
            doubleton_code.pop(code)

# print frequent items
for i in item_count:
    print(list(product_code.keys())[list(product_code.values()).index(i)])

# return the previous name to the products
for key, value in doubleton_code.items():
    for j in range(2):
        doubleton_code[key][j] = list(product_code.keys())[list(product_code.values()).index(doubleton_code[key][j])]

# print frequent doubletons
for i in doubleton_code.values():
    print(i)

