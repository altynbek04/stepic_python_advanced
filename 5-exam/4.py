n = int(input())

matrix = [['.'] * n for _ in range(n)]
mid = n // 2

for i in range(n):
    for j in range(n):
        if i == j or i + j == n - 1 or i == mid or j == mid:
            matrix[i][j] = '*'

for row in matrix:
    print(*row)
