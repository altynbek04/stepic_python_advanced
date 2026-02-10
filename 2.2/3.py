nums = list(map(int, input().split()))
for i in range(len(nums)):
    if i % 2 == 0 and i + 1 < len(nums):
        nums[i], nums[i + 1] = nums[i + 1], nums[i]

print(*nums)
