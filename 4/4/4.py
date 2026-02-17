n = int(input())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))

summetric = True

for i in range(n):
    for j in range(n):
        if matrix[i][j] != matrix[j][i]:
            summetric = False

if summetric:
    print("YES")
else:
    print("NO")