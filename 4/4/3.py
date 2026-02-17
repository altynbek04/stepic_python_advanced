n = int(input())
m = int(input())
matrix = []

for _ in range(n):
    matrix.append(list(map(int, input().split())))

i, j = map(int, input().split())


for row in matrix:
    row[i], row[j] = row[j], row[i]

for row in matrix:
    print(*row)