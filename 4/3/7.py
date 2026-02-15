n = int(input())

top = 0
right = 0
bottom = 0
left = 0

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if i < j and i < n - 1 - j:
            top += row[j]
        elif i < j and i > n - 1 - j:
            right += row[j]
        elif i > j and i > n - 1 - j:
            bottom += row[j]
        elif i > j and i < n - 1 - j:
            left += row[j]

print(f"Верхняя четверть: {top}")
print(f"Правая четверть: {right}")
print(f"Нижняя четверть: {bottom}")
print(f"Левая четверть: {left}")