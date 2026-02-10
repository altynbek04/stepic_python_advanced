
n = input()
res = []
while len(n) > 3:
    res.append(n[-3:])
    n = n[:-3]
res.append(n)
print(",".join(res[::-1]))


