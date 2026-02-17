n = int(input())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))

for i in range(n):
    matrix[i][i], matrix[n - i -1][i] = matrix[n - i - 1][i], matrix[i][i]

for row in matrix:
    print(*row)