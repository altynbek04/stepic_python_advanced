n, m = map(int, input().split())

num = 1

for i in range(n):
    row = []
    for j in range(m):
        row.append(num)
        num += 1
    if i % 2 == 1:
        row.reverse()

    for x in row:
        print(str(x).ljust(3), end='')
    print()
