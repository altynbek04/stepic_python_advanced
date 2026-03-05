text = input().lower()

for ch in '.,;:-?!':
    text = text.replace(ch, '')

words = text.split()
print(len(set(words)))