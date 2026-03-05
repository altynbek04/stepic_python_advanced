s1, s2, s3 = input().split()

set1 = set(s1)
set2 = set(s2)
set3 = set(s3)

if set1 == set2 == set3:
    print("YES")
else:
    print("NO")