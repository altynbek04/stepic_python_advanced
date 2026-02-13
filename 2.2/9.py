s = input()

parts = s.split("О")

max_r = 0
for p in parts:
    max_r = max(max_r, len(p))

print(max_r)