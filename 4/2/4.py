def pascal(n):
    row = [1]
    for k in range(1, n + 1):
        row.append(row[k - 1] * (n - k + 1) // k)
    return row

n = int(input())
print(pascal(n))
