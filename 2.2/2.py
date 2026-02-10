nums = list(map(int, input().split()))
count = 0
for num in range(1, len(nums)):
    if nums[num] > nums[num - 1]:
        count += 1
print(count)