def func(num1, num2):
    return num1 % num2 == 0

a = int(input())
b = int(input())
if func(a, b):
    print("делится")
else:
    print("не делится")