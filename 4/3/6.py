n = int(input())
max_el = -10**9

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if i >= j and i <= n - 1 - j or i <= j and i >= n - 1 - j:
            max_el = max(max_el, row[j])
print(max_el)