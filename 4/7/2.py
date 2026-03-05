n,m = map(int, input().split())

a = []
for _ in range(n):
    a.append(list(map(int, input().split())))

input()

m2,k = map(int, input().split())

b = []
for _ in range(m):
    b.append(list(map(int, input().split())))

c = [[0] * k for _ in range(n)]
for i in range(n):
    for j in range(n):
        for k in range(m):
            c[i][j] += a[i][k] * b[k][j]
for row in c:
    print(*row)
