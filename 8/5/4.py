numbers = input().split()
seen = set()

for num in numbers:
    num = int(num)
    if num in seen:
        print("YES")
    else:
        print("NO")
        seen.add(num)