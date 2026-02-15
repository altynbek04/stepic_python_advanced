n = int(input())
total = 0

for i in range(n):
    row = list(map(int, input().split()))
    total += row[i]
print(total)