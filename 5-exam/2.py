n = int(input())

matrix = []
for i in range(n):
    matrix.append(list(map(int, input().split())))
maximum = -10**9
for i in range(n):
    for j in range(n):
        if i + j >= n - 1:
            maximum = max(maximum, matrix[i][j])
print(maximum)