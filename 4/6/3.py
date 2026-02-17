n , m = map(int, input().split())

num = 1
for i in range(n):
    row = []
    for j in range(m):
        print(str(num).ljust(3), end='')
        num += 1
    print(*row)
