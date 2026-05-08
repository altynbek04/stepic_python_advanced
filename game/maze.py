import pygame
import random

CELL = 25
W, H = 21, 21

maze = [["#"] * W for _ in range(H)]

def carve(x, y):
    maze[y][x] = " "
    dirs = [(2,0),(-2,0),(0,2),(0,-2)]
    random.shuffle(dirs)

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 1 <= nx < W-1 and 1 <= ny < H-1 and maze[ny][nx] == "#":
            maze[y + dy//2][x + dx//2] = " "
            carve(nx, ny)

carve(1,1)

player = [1,1]

pygame.init()
screen = pygame.display.set_mode((W*CELL, H*CELL))

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            dx, dy = 0,0
            if e.key == pygame.K_w: dy = -1
            if e.key == pygame.K_s: dy = 1
            if e.key == pygame.K_a: dx = -1
            if e.key == pygame.K_d: dx = 1

            nx = player[0] + dx
            ny = player[1] + dy

            if maze[ny][nx] == " ":
                player = [nx, ny]

    screen.fill((0,0,0))

    for y in range(H):
        for x in range(W):
            if maze[y][x] == "#":
                pygame.draw.rect(screen, (120,120,120),
                                 (x*CELL, y*CELL, CELL, CELL))

    pygame.draw.rect(screen, (0,255,0),
                     (player[0]*CELL, player[1]*CELL, CELL, CELL))

    pygame.display.flip()

pygame.quit()