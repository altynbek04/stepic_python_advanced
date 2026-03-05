n = int(input())
chars = set()

for _ in range(n):
    word = input().lower()
    chars.update(word)

print(len(chars))