n, m = map(int, input().split())

for i in range(n):
    for j in range(m):
        num = i + 1 + j * n
        print(str(num).ljust(3), end='')
    print()