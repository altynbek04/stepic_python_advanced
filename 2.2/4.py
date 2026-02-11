nums = input().split()

nums = [nums[-1]] + nums[:-1]

print(*nums)