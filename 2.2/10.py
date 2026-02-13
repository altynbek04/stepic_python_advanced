n = int(input())
virus = "anton"

ans = []

for i in range(1, n + 1):
    s = input()
    j = 0

    for ch in s:
        if ch == virus[j]:
            j += 1
            if j == len(virus):
                ans.append(i)
                break
print(*ans)