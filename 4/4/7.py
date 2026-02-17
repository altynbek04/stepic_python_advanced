n = int(input())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))

new_matrix = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        new_matrix[j][n - i - 1] = matrix[i][j]
for row in new_matrix:
    print(*row)