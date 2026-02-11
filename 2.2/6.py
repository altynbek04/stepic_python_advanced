n = int(input())
nums = []

for _ in range(n):
    nums.append(int(input()))

target = int(input())

found = False
for i in range(n):
    for j in range(i+1, n):
        if nums[i] * nums[j] == target:
            found = True
            break
    if found:
        break
if found:
    print("ДА")
else:
    print("НЕТ")
