s = input().split()

result = []

group = [s[0]]

for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        group.append(s[i])
    else:
        result.append(group)
        group = [s[i]]
result.append(group)
print(result)