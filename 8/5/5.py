n = int(input())

correct_users = set()
correct_attempts = 0

for _ in range(n):
    line = input()
    name, result = line.split(': ')

    if result == 'Correct':
        correct_attempts += 1
        correct_users.add(name)

if correct_attempts == 0:
    print("Вы можете стать первым, кто решит эту задачу")
else:
    percent = int(correct_attempts * 100 / n + 0.5)
    print(f"Верно решили {len(correct_users)} учащихся")
    print(f"Из всех попыток {percent}% верных")
