def multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


n = int(input())
A = [list(map(int, input().split())) for _ in range(n)]
m = int(input())

# единичная матрица
result = [[0] * n for _ in range(n)]
for i in range(n):
    result[i][i] = 1

# A^m
for _ in range(m):
    result = multiply(result, A)

for row in result:
    print(*row)
