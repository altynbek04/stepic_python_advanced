s = input()
n = input()
r = s + n

unique = set(r)

if len(unique) == 10:
    print('YES')
else:
    print('NO')