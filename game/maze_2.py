import pygame
import numpy as np
import random
from collections import deque

# ------------------ НАСТРОЙКИ ------------------
WIDTH, HEIGHT = 600, 600
PLAYER_SIZE = 30
OBJECT_SIZE = 20

N_GREENS = 5  # зелёные (полезные)
N_REDS = 4  # красные (опасные)

ALPHA = 0.7
GAMMA = 0.95
EPS = 1.0
EPS_MIN = 0.05
EPS_DECAY = 0.998
EPISODES = 1500
MAX_STEPS = 400

STEP_PENALTY = -0.03
GREEN_REWARD = 1.0
RED_PENALTY = -1.0

# Действия: 0-влево, 1-вправо, 2-вверх, 3-вниз
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
N_ACTIONS = 4

# Дискретизация состояния: позиция игрока (10x10) + смещения до ближайших объектов
# Упростим: состояние = (x_cell, y_cell, dx_green, dy_green, dx_red, dy_red)
GRID_SIZE = 10
CELL_W = WIDTH // GRID_SIZE
CELL_H = HEIGHT // GRID_SIZE

# ------------------ ИНИЦИАЛИЗАЦИЯ ОКРУЖЕНИЯ ------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)


class Environment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = [WIDTH // 2, HEIGHT // 2]
        self.greens = []
        self.reds = []
        for _ in range(N_GREENS):
            self.greens.append(self._random_pos(OBJECT_SIZE))
        for _ in range(N_REDS):
            self.reds.append(self._random_pos(OBJECT_SIZE))
        self.done = False
        self.step_count = 0
        return self._get_state()

    def _random_pos(self, size):
        return [random.randint(0, WIDTH - size), random.randint(0, HEIGHT - size)]

    def _get_state(self):
        # Дискретизация позиции игрока
        px = self.player[0] // CELL_W
        py = self.player[1] // CELL_H
        px = min(px, GRID_SIZE - 1)
        py = min(py, GRID_SIZE - 1)

        # Найти ближайший зелёный шар
        if self.greens:
            gx, gy = min(self.greens, key=lambda p: abs(p[0] - self.player[0]) + abs(p[1] - self.player[1]))
            dgx = (gx - self.player[0]) // CELL_W
            dgy = (gy - self.player[1]) // CELL_H
            dgx = max(-5, min(5, dgx)) + 5  # сдвиг в 0..10
            dgy = max(-5, min(5, dgy)) + 5
        else:
            dgx, dgy = 5, 5

        # Найти ближайший красный шар
        if self.reds:
            rx, ry = min(self.reds, key=lambda p: abs(p[0] - self.player[0]) + abs(p[1] - self.player[1]))
            drx = (rx - self.player[0]) // CELL_W
            dry = (ry - self.player[1]) // CELL_H
            drx = max(-5, min(5, drx)) + 5
            dry = max(-5, min(5, dry)) + 5
        else:
            drx, dry = 5, 5

        return (px, py, dgx, dgy, drx, dry)

    def step(self, action):
        self.step_count += 1
        dx, dy = ACTIONS[action]
        self.player[0] += dx * 8
        self.player[1] += dy * 8
        self.player[0] = max(0, min(WIDTH - PLAYER_SIZE, self.player[0]))
        self.player[1] = max(0, min(HEIGHT - PLAYER_SIZE, self.player[1]))

        reward = STEP_PENALTY

        # Проверка столкновений с зелёными
        for g in self.greens[:]:
            if self._collide(self.player, PLAYER_SIZE, g, OBJECT_SIZE):
                self.greens.remove(g)
                reward += GREEN_REWARD
                # добавить новый зелёный шар
                self.greens.append(self._random_pos(OBJECT_SIZE))

        # Проверка столкновений с красными
        for r in self.reds[:]:
            if self._collide(self.player, PLAYER_SIZE, r, OBJECT_SIZE):
                self.reds.remove(r)
                reward += RED_PENALTY
                self.reds.append(self._random_pos(OBJECT_SIZE))

        if self.step_count >= MAX_STEPS:
            self.done = True

        return self._get_state(), reward, self.done

    def _collide(self, p1, s1, p2, s2):
        return (abs(p1[0] - p2[0]) < (s1 + s2) and abs(p1[1] - p2[1]) < (s1 + s2))

    def render(self, screen):
        screen.fill((0, 0, 0))
        # Игрок
        pygame.draw.rect(screen, (0, 255, 255), (*self.player, PLAYER_SIZE, PLAYER_SIZE))
        # Зелёные
        for g in self.greens:
            pygame.draw.circle(screen, (0, 255, 0), (g[0] + OBJECT_SIZE // 2, g[1] + OBJECT_SIZE // 2),
                               OBJECT_SIZE // 2)
        # Красные
        for r in self.reds:
            pygame.draw.circle(screen, (255, 0, 0), (r[0] + OBJECT_SIZE // 2, r[1] + OBJECT_SIZE // 2),
                               OBJECT_SIZE // 2)
        # Текст
        text = font.render(f"Зелёных: {len(self.greens)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        text2 = font.render(f"Красных: {len(self.reds)}", True, (255, 255, 255))
        screen.blit(text2, (10, 30))


# ------------------ Q-LEARNING ------------------
def encode_state(state):
    # state = (px, py, dgx, dgy, drx, dry) все от 0 до 9
    return state[0] * 10 ** 5 + state[1] * 10 ** 4 + state[2] * 10 ** 3 + state[3] * 10 ** 2 + state[4] * 10 + state[5]


# Размер таблицы: 10*10*11*11*11*11 ~ 1.4 млн возможно, но используется разреженно. Для простоты используем словарь.
Q = {}


def get_Q(state, action):
    s = encode_state(state)
    if (s, action) not in Q:
        Q[(s, action)] = 0.0
    return Q[(s, action)]


def set_Q(state, action, value):
    s = encode_state(state)
    Q[(s, action)] = value


# График
episode_rewards = []
avg_rewards = []
window = deque(maxlen=50)

env = Environment()
for ep in range(EPISODES):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Выбор действия
        if random.random() < EPS:
            action = random.randint(0, N_ACTIONS - 1)
        else:
            q_vals = [get_Q(state, a) for a in range(N_ACTIONS)]
            action = np.argmax(q_vals)

        next_state, reward, done = env.step(action)
        total_reward += reward

        # Q-learning обновление
        best_next = max([get_Q(next_state, a) for a in range(N_ACTIONS)]) if not done else 0
        td_target = reward + GAMMA * best_next
        td_error = td_target - get_Q(state, action)
        new_q = get_Q(state, action) + ALPHA * td_error
        set_Q(state, action, new_q)

        state = next_state

        # Отрисовка
        env.render(screen)
        info = font.render(f"Эпизод {ep} | Награда: {total_reward:.1f} | ε={EPS:.2f}", True, (200, 200, 200))
        screen.blit(info, (10, HEIGHT - 30))
        pygame.display.flip()
        clock.tick(60)

    episode_rewards.append(total_reward)
    window.append(total_reward)
    avg_rewards.append(sum(window) / len(window))

    EPS = max(EPS_MIN, EPS * EPS_DECAY)

    if ep % 100 == 0:
        print(f"Эпизод {ep}, награда: {total_reward:.2f}, средняя за 50: {avg_rewards[-1]:.2f}, ε={EPS:.3f}")

print("Обучение закончено!")
pygame.quit()