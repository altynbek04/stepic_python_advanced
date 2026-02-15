n = int(input())

lst = []

for i in range(1, n + 1):
    lst.append(list(range(1, i + 1)))

for row in lst:
    print(row)