s = input()

total = len(s) * 60  # в копейках

rub = total // 100
kop = total % 100

print(f"{rub} р. {kop} коп.")