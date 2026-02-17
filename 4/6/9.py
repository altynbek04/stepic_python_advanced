n,m = map(int, input().split())
matrix = [[0]* m for _ in range(n)]
num = 1
for s in range(n + m - 1):
    for i in range(n):
        j = s - i
        if 0 <= j < m:
            matrix[i][j] = num
            num += 1
for row in matrix:
    for x in row:
        print(str(x).ljust(3), end='')
    print()