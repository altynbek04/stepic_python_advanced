n = int(input())

for i in range(n):
    row = []
    for j in range(n):
        if i + j == n -1:
            row.append(1)
        elif i == j:
            row.append(1)
        else:
            row.append(0)
    print(*row)