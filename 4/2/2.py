n = int(input())

lst = []

for _ in range(n):
    lst.append(list(range(1, n + 1)))

for row in lst:
    print(row)