n = int(input())
m = int(input())

mult = []
for i in range(n):
    row = []
    for j in range(m):
        row.append(i * j)
    mult.append(row)

for row in mult:
    for col in row:
        print(str(col).ljust(3), end='')
    print()