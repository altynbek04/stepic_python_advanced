n, m = map(int, input().split())

for i in range(n):
    row = []
    for j in range(m):
        row.append((i + j) % m + 1)
    print(*row)