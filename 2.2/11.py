word = input()
s = word + " запретил букву"

letters = sorted(set(s.replace(" ", "")))

for ch in letters:
    print(s, ch)
    s = s.replace(ch, "")
    s = " ".join(s.split())

