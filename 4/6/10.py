n, m = map(int, input().split())

matrix = [[0] * m for _ in range(n)]

top = 0
bottom = n - 1
left = 0
right = m - 1

num = 1

while num <= n * m:
    # слева направо
    for j in range(left, right + 1):
        matrix[top][j] = num
        num += 1
    top += 1

    # сверху вниз
    for i in range(top, bottom + 1):
        matrix[i][right] = num
        num += 1
    right -= 1

    # справа налево
    if top <= bottom:
        for j in range(right, left - 1, -1):
            matrix[bottom][j] = num
            num += 1
        bottom -= 1

    # снизу вверх
    if left <= right:
        for i in range(bottom, top - 1, -1):
            matrix[i][left] = num
            num += 1
        left += 1

for row in matrix:
    for x in row:
        print(str(x).ljust(3), end='')
    print()
