n = int(input())

for i in range(n):
    row = []
    for j in range(n):
        if i + j == n -1:
            row.append(1)
        elif i + j < n -1:
            row.append(0)
        elif i + j > n -1:
            row.append(2)
    print(*row)