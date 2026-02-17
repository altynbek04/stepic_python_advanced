n = int(input())
a = [list(map(int, input().split())) for _ in range(n)]

nums = [x for row in a for x in row]
if sorted(nums) != list(range(1, n*n + 1)):
    print("NO")
    exit()

magic = sum(a[0])
for i in range(n):
    if sum(a[i]) != magic:
        print("NO")
        exit()
for j in range(n):
    if sum(a[i][j] for i in range(n)) != magic:
        print("NO")
        exit()
if sum(a[i][i] for i in range(n)) != magic:
    print("NO")
    exit()

if sum(a[i][n - i - 1] for i in range(n)) != magic:
    print("NO")
    exit()
print("YES")