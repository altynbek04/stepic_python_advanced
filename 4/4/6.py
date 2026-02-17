n = int(input())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))
matrix.reverse()
for row in matrix:
    print(*row)