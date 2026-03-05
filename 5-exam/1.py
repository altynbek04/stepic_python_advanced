s = input().split()
n = int(input())

result = [[] for _ in range(n)]

for i in range(len(s)):
    result[i % n].append(s[i])
print(result)
