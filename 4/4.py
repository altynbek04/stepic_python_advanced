list1 = [[7, 15], [2, 3, 5, 10], [4]]

mx = list1[0][0]

for sub in list1:
    mx = max(mx, max(sub))

print(mx)
