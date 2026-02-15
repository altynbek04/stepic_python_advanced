list1 = [[1, 7, 8], [9, 7, 102], [102, 106, 105], [100, 99, 98, 103], [1, 2, 3]]
total = 0
count = 0

for sub in list1:
    total += sum(sub)
    count += len(sub)

print(total / count)