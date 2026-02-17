n = int(input())
m = int(input())

maximum = None
max_row = 0
max_col = 0

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(m):
        if maximum is None or row[j] > maximum:
            maximum = row[j]
            max_row = i
            max_col = j
print(max_row, max_col)