import pygame
import numpy as np
import random
from collections import deque

# ---------------- НОРМАЛЬНЫЙ ЛАБИРИНТ ----------------
GRID_TEMPLATE = [
    [0,0,0,0,0,0,0,2],
    [0,1,1,1,0,1,1,0],
    [0,0,0,1,0,0,0,0],
    [2,1,0,1,1,1,0,2],
    [0,1,0,0,0,1,0,0],
    [0,1,1,1,0,1,1,0],
    [2,0,0,0,0,0,0,2],
    [0,1,1,1,1,1,0,0],
]

ROWS = len(GRID_TEMPLATE)
COLS = len(GRID_TEMPLATE[0])

ACTIONS = [(-1,0),(0,1),(1,0),(0,-1)]
N_ACTIONS = 4

# ---------------- ПАРАМЕТРЫ ----------------
ALPHA = 0.6
GAMMA = 0.95

EPS = 1.0
EPS_MIN = 0.05
EPS_DECAY = 0.995

EPISODES = 2000
MAX_STEPS = 200

STEP_PENALTY = -0.03
WALL_PENALTY = -0.2
COIN_REWARD = 1.0

# ---------------- ВИЗУАЛ ----------------
CELL = 50
GRAPH_W = 300

WIDTH = COLS * CELL + GRAPH_W
HEIGHT = ROWS * CELL

WHITE = (220,220,220)
BLACK = (0,0,0)
GRAY = (100,100,100)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,150,255)
ORANGE = (255,150,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-learning AI")

font = pygame.font.SysFont("Arial", 16)

# ---------------- Q ----------------
Q = np.zeros((ROWS, COLS, N_ACTIONS))


def reset_grid():
    return [row[:] for row in GRID_TEMPLATE]


def random_start(grid):
    while True:
        x = random.randint(0, ROWS-1)
        y = random.randint(0, COLS-1)
        if grid[x][y] == 0:
            return x, y


def step(grid, x, y, action):
    dx, dy = ACTIONS[action]
    nx, ny = x + dx, y + dy

    if nx < 0 or nx >= ROWS or ny < 0 or ny >= COLS:
        return x, y, WALL_PENALTY, False

    if grid[nx][ny] == 1:
        return x, y, WALL_PENALTY, False

    if grid[nx][ny] == 2:
        grid[nx][ny] = 0
        return nx, ny, COIN_REWARD, True

    return nx, ny, STEP_PENALTY, False


def count_coins(grid):
    return sum(row.count(2) for row in grid)


# ---------------- ГРАФИК ----------------
rewards = []
avg_rewards = []
window = deque(maxlen=50)


def draw_graph():
    base_x = COLS * CELL

    pygame.draw.rect(screen, (30,30,30), (base_x, 0, GRAPH_W, HEIGHT))

    if len(rewards) < 2:
        return

    max_r = max(rewards)
    min_r = min(rewards)

    def scale(val):
        return HEIGHT - int((val - min_r) / (max_r - min_r + 1e-5) * HEIGHT)

    for i in range(1, len(rewards)):
        x1 = base_x + int((i-1)/len(rewards)*GRAPH_W)
        x2 = base_x + int(i/len(rewards)*GRAPH_W)

        pygame.draw.line(screen, BLUE,
                         (x1, scale(rewards[i-1])),
                         (x2, scale(rewards[i])))

        pygame.draw.line(screen, ORANGE,
                         (x1, scale(avg_rewards[i-1])),
                         (x2, scale(avg_rewards[i])))


# ---------------- ОБУЧЕНИЕ ----------------
clock = pygame.time.Clock()

for ep in range(EPISODES):

    grid = reset_grid()
    x, y = random_start(grid)
    coins_left = count_coins(grid)

    total_reward = 0

    for step_i in range(MAX_STEPS):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if random.random() < EPS:
            action = random.randint(0,3)
        else:
            action = np.argmax(Q[x, y])

        nx, ny, reward, got_coin = step(grid, x, y, action)

        Q[x, y, action] += ALPHA * (
            reward + GAMMA * np.max(Q[nx, ny]) - Q[x, y, action]
        )

        x, y = nx, ny
        total_reward += reward

        if got_coin:
            coins_left -= 1

        if coins_left == 0:
            break

        # ---- отрисовка ----
        screen.fill(BLACK)

        for i in range(ROWS):
            for j in range(COLS):
                rect = (j*CELL, i*CELL, CELL, CELL)

                if grid[i][j] == 1:
                    pygame.draw.rect(screen, GRAY, rect)
                elif grid[i][j] == 2:
                    pygame.draw.rect(screen, YELLOW, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)

                pygame.draw.rect(screen, BLACK, rect, 1)

        pygame.draw.circle(
            screen, GREEN,
            (y*CELL + CELL//2, x*CELL + CELL//2),
            CELL//3
        )

        draw_graph()

        text = font.render(f"Ep {ep} step {step_i} eps {EPS:.3f}", True, (255,255,255))
        screen.blit(text, (COLS*CELL + 10, 10))

        pygame.display.flip()
        clock.tick(60)

    rewards.append(total_reward)
    window.append(total_reward)
    avg_rewards.append(sum(window)/len(window))

    EPS = max(EPS_MIN, EPS * EPS_DECAY)

    if ep % 100 == 0:
        print(f"Ep {ep} reward={round(total_reward,2)} eps={round(EPS,3)}")

print("Обучение завершено")

pygame.quit()