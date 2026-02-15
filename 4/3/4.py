n = int(input())

for i in range(n):
    row = list(map(int, input().split()))
    avg = sum(row) / len(row)

    count = 0
    for num in row:
        if num > avg:
            count += 1

    print(count)