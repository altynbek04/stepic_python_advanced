import pygame
import numpy as np
import random
from collections import deque

# ------------------ НАСТРОЙКИ ИГРЫ ------------------
ROWS, COLS = 10, 10
CELL_SIZE = 60
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Действия: 0-вверх, 1-вправо, 2-вниз, 3-влево
ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
N_ACTIONS = 4

# Параметры Q-learning
ALPHA = 0.7  # скорость обучения
GAMMA = 0.95  # дисконт будущей награды
EPS = 1.0  # начальный epsilon
EPS_MIN = 0.05
EPS_DECAY = 0.995
EPISODES = 2000
MAX_STEPS = 150

# Награды
STEP_PENALTY = -0.02
TREASURE_REWARD = 5
TRAP_PENALTY = -3
EXIT_REWARD = 10


# ------------------ ОКРУЖЕНИЕ ------------------
class TreasureHuntEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        # Генерация карты: 0-пусто, 1-стена, 2-сундук, 3-ловушка, 4-выход
        self.grid = self._generate_map()
        self.start_pos = self._random_free_cell()
        self.player_pos = list(self.start_pos)
        self.done = False
        self.steps = 0
        self.score = 0
        return self._get_state()

    def _generate_map(self):
        # Простой лабиринт с комнатами, стенами, сокровищами и ловушками
        grid = np.zeros((ROWS, COLS), dtype=int)
        # Стены по краям
        for i in range(ROWS):
            grid[i][0] = 1
            grid[i][COLS - 1] = 1
        for j in range(COLS):
            grid[0][j] = 1
            grid[ROWS - 1][j] = 1

        # Внутренние стены (лабиринт)
        for i in range(2, ROWS - 2, 2):
            for j in range(2, COLS - 2, 2):
                grid[i][j] = 1
        # Добавим случайные стены
        for _ in range(20):
            r = random.randint(1, ROWS - 2)
            c = random.randint(1, COLS - 2)
            if grid[r][c] == 0:
                grid[r][c] = 1

        # Размещаем сундуки (2)
        for _ in range(5):
            r, c = self._random_free_cell(grid)
            grid[r][c] = 2

        # Ловушки (3)
        for _ in range(4):
            r, c = self._random_free_cell(grid)
            grid[r][c] = 3

        # Выход (4) - только один
        r, c = self._random_free_cell(grid)
        grid[r][c] = 4

        return grid

    def _random_free_cell(self, grid=None):
        if grid is None:
            grid = self.grid
        while True:
            r = random.randint(1, ROWS - 2)
            c = random.randint(1, COLS - 2)
            if grid[r][c] == 0:
                return (r, c)

    def _get_state(self):
        # Состояние = позиция игрока (row, col) – дискретно, просто индексы
        return (self.player_pos[0], self.player_pos[1])

    def step(self, action):
        self.steps += 1
        dr, dc = ACTIONS[action]
        nr, nc = self.player_pos[0] + dr, self.player_pos[1] + dc

        reward = STEP_PENALTY

        # Проверка стены
        if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS or self.grid[nr][nc] == 1:
            return self._get_state(), reward, self.done  # не двигаемся

        # Двигаемся
        self.player_pos = [nr, nc]
        cell = self.grid[nr][nc]

        if cell == 2:  # сундук
            reward += TREASURE_REWARD
            self.grid[nr][nc] = 0  # забрали
            self.score += 1
        elif cell == 3:  # ловушка
            reward += TRAP_PENALTY
            # отбросить назад (наказание)
            self.player_pos = list(self.start_pos)  # возврат на старт
        elif cell == 4:  # выход
            reward += EXIT_REWARD
            self.done = True

        if self.steps >= MAX_STEPS:
            self.done = True

        return self._get_state(), reward, self.done

    def render(self, screen, font):
        # Отрисовка сетки
        for i in range(ROWS):
            for j in range(COLS):
                rect = (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = self.grid[i][j]
                if cell == 1:
                    pygame.draw.rect(screen, (80, 80, 80), rect)
                elif cell == 2:
                    pygame.draw.rect(screen, (255, 215, 0), rect)  # золото
                    text = font.render("💰", True, (0, 0, 0))
                    screen.blit(text, (j * CELL_SIZE + 10, i * CELL_SIZE + 10))
                elif cell == 3:
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # ловушка
                    text = font.render("⚡", True, (255, 255, 255))
                    screen.blit(text, (j * CELL_SIZE + 15, i * CELL_SIZE + 15))
                elif cell == 4:
                    pygame.draw.rect(screen, (0, 200, 0), rect)  # выход
                    text = font.render("🚪", True, (0, 0, 0))
                    screen.blit(text, (j * CELL_SIZE + 15, i * CELL_SIZE + 15))
                else:
                    pygame.draw.rect(screen, (220, 220, 220), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Агент
        r, c = self.player_pos
        pygame.draw.circle(screen, (0, 100, 255), (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 3)

        # Информация
        info = font.render(f"Собрано: {self.score} | Шаг: {self.steps}", True, (0, 0, 0))
        screen.blit(info, (10, 10))


# ------------------ Q-LEARNING ------------------
Q = np.zeros((ROWS, COLS, N_ACTIONS))


def get_action(state):
    if random.random() < EPS:
        return random.randint(0, N_ACTIONS - 1)
    else:
        r, c = state
        return np.argmax(Q[r, c])


# Графики
episode_rewards = []
avg_rewards = []
window = deque(maxlen=50)

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt - Q-learning AI")
font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()

env = TreasureHuntEnv()

for ep in range(EPISODES):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        action = get_action(state)
        next_state, reward, done = env.step(action)
        total_reward += reward

        # Q-learning update
        r, c = state
        nr, nc = next_state
        best_next = np.max(Q[nr, nc]) if not done else 0
        Q[r, c, action] += ALPHA * (reward + GAMMA * best_next - Q[r, c, action])

        state = next_state

        # Отрисовка
        screen.fill((255, 255, 255))
        env.render(screen, font)
        text = font.render(f"Эпизод {ep} | Награда: {total_reward:.1f} | ε={EPS:.3f}", True, (0, 0, 0))
        screen.blit(text, (10, HEIGHT - 30))
        pygame.display.flip()
        clock.tick(60)

    episode_rewards.append(total_reward)
    window.append(total_reward)
    avg_rewards.append(sum(window) / len(window))

    EPS = max(EPS_MIN, EPS * EPS_DECAY)

    if ep % 100 == 0:
        print(f"Эпизод {ep}, награда: {total_reward:.2f}, средняя за 50: {avg_rewards[-1]:.2f}, ε={EPS:.3f}")

print("Обучение завершено! Наблюдай за лучшей стратегией...")

# Демонстрация лучшей политики (epsilon = 0)
EPS = 0.0
env = TreasureHuntEnv()
state = env.reset()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    r, c = state
    action = np.argmax(Q[r, c])
    state, _, done = env.step(action)
    screen.fill((255, 255, 255))
    env.render(screen, font)
    pygame.display.flip()
    clock.tick(10)  # медленно для просмотра

pygame.quit()