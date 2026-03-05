n = int(input())
for _ in range(n):
    word = input().lower()
    unique_chars = set(word)
    print(len(unique_chars))