n = int(input())

for i in range(n):
    for j in range(n):
        if i <= j <= n - i - 1 or n - i - 1 <= j <= i:
            print("1".ljust(3), end='')
        else:
            print("0".ljust(3), end='')
    print()