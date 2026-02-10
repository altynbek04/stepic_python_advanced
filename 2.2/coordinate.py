s = int(input())

count1 = count2 = count3 = count4 = 0

for _ in range(s):
    x, y = map(int, input().split())

    if x > 0 and y > 0:
        count1 += 1
    elif x < 0 and y > 0:
        count2 += 1
    elif x < 0 and y < 0:
        count3 += 1
    elif x > 0 and y < 0:
        count4 += 1

print(f"Первая четверть: {count1}")
print(f"Вторая четверть: {count2}")
print(f"Третья четверть: {count3}")
print(f"Четвертая четверть: {count4}")
