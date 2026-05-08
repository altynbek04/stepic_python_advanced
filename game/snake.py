import pygame
import random
import sys
from collections import deque

# ---------- НАСТРОЙКИ ----------
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (200, 200, 200)
DARK_GREEN = (0, 150, 0)

# Направления: 0-вверх, 1-вправо, 2-вниз, 3-влево
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake - змейка с искусственным интеллектом")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


class SnakeAI:
    def __init__(self):
        self.reset()

    def reset(self):
        # Начальная змейка (голова в центре)
        start_x = GRID_SIZE // 2
        start_y = GRID_SIZE // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = 1  # вправо
        self.grow = False
        self.score = 0
        self.steps_without_food = 0
        self.generate_food()

    def generate_food(self):
        # Еда не должна появляться на теле змейки
        free_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if (x, y) not in self.body]
        if free_cells:
            self.food = random.choice(free_cells)
        else:
            self.food = None  # победа (всё поле заполнено)

    def move(self, new_dir):
        # Меняем направление, если не противоположное
        if (new_dir == 0 and self.direction != 2) or \
                (new_dir == 1 and self.direction != 3) or \
                (new_dir == 2 and self.direction != 0) or \
                (new_dir == 3 and self.direction != 1):
            self.direction = new_dir

        dx, dy = DIRS[self.direction]
        head = self.body[0]
        new_head = (head[0] + dx, head[1] + dy)

        # Вставляем новую голову
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        # Проверка столкновений
        if self.is_collision():
            return False

        # Съела ли еду?
        if new_head == self.food:
            self.score += 1
            self.grow = True
            self.steps_without_food = 0
            self.generate_food()
            if self.food is None:  # победа
                return True
        else:
            self.steps_without_food += 1
            # Если слишком долго без еды (зациклился) – проигрыш
            if self.steps_without_food > GRID_SIZE * GRID_SIZE * 2:
                return False
        return True

    def is_collision(self):
        head = self.body[0]
        # Стены
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            return True
        # Столкновение с собой (кроме первого сегмента, т.к. голова может совпасть только если играли без учёта)
        if head in self.body[1:]:
            return True
        return False

    # ---------- AI ЛОГИКА ----------
    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                # Для поиска пути учитываем только свободные клетки (не тело змейки)
                # Но голову считаем свободной, а хвост после движения освободится
                if (nx, ny) not in self.body[1:]:
                    neighbors.append((nx, ny))
        return neighbors

    def bfs_path(self, start, target):
        """Возвращает кратчайший путь от start до target (список клеток от start до target) или None"""
        if start == target:
            return []
        queue = deque([(start, [start])])
        visited = set([start])
        while queue:
            node, path = queue.popleft()
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    if neighbor == target:
                        return path + [neighbor]
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def is_safe_move(self, direction):
        """Проверяет, не приведёт ли движение в direction к немедленной смерти"""
        dx, dy = DIRS[direction]
        head = self.body[0]
        new_head = (head[0] + dx, head[1] + dy)
        # Стена
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            return False
        # Столкновение с телом (исключая хвост, который может уйти)
        if new_head in self.body[1:]:
            # Если хвост – можно, если мы не растем
            if not (self.grow == False and new_head == self.body[-1]):
                return False
        return True

    def get_next_direction(self):
        # 1. Пытаемся найти путь к еде
        path_to_food = self.bfs_path(self.body[0], self.food)
        if path_to_food and len(path_to_food) > 1:
            next_cell = path_to_food[1]
            # Находим направление к next_cell
            dx = next_cell[0] - self.body[0][0]
            dy = next_cell[1] - self.body[0][1]
            for idx, (ddx, ddy) in enumerate(DIRS):
                if (ddx, ddy) == (dx, dy):
                    desired_dir = idx
                    break
            # Проверяем, безопасно ли это движение
            if self.is_safe_move(desired_dir):
                return desired_dir

        # 2. Если нет безопасного пути к еде – ищем самое безопасное направление (путь к хвосту или любой выживающий)
        # Попробуем все направления, выберем то, которое не ведёт к смерти
        safe_dirs = []
        for d in range(4):
            if self.is_safe_move(d):
                safe_dirs.append(d)

        if safe_dirs:
            # Можно дополнительно выбрать то, которое ближе к еде, но не обязательно
            # Просто первое безопасное (вверх, вправо, вниз, влево)
            return safe_dirs[0]

        # 3. Всё плохо – любое направление (умираем)
        return self.direction  # сохраняем текущее


# ------------------ ОСНОВНАЯ ИГРА ------------------
snake = SnakeAI()
auto_mode = True  # AI управляет
running = True
game_over = False
demo_mode = True  # показываем работу AI

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                snake = SnakeAI()
                game_over = False
            if event.key == pygame.K_m:
                auto_mode = not auto_mode
                print("Режим:", "AI" if auto_mode else "Ручной (стрелки)")
            if not auto_mode and not game_over:
                # Ручное управление
                if event.key == pygame.K_UP:
                    snake.move(0)
                elif event.key == pygame.K_RIGHT:
                    snake.move(1)
                elif event.key == pygame.K_DOWN:
                    snake.move(2)
                elif event.key == pygame.K_LEFT:
                    snake.move(3)

    if not game_over:
        if auto_mode:
            # AI выбирает направление
            next_dir = snake.get_next_direction()
            game_over = not snake.move(next_dir)
        else:
            # В ручном режиме движение уже обработано в событиях, но нужно продолжать?
            # В ручном режиме надо вызывать move только при нажатии, но тогда змейка не движется.
            # Упростим: в ручном режиме змейка движется с частотой кадров с последним выбранным направлением.
            # Для этого сохраним последнее направление из событий.
            # Переделаем: если ручной режим, то в событии меняем snake.direction, а вызов move делаем здесь один раз за кадр с текущим direction.
            # Реализуем:
            # Уже выше: в ручном режиме при нажатии стрелки вызывается snake.move(направление). Это нормально, но move делает шаг.
            # Чтобы движение было плавным, нужно ограничить скорость.
            pass  # Т.к. в ручном режиме move вызывается по нажатию, змейка стоит – это неудобно.
            # Исправим: вынесем move из событий, а в событиях будем менять snake.direction.
            # Сделаем проще: при ручном режиме используем обычное управление с клавиш, но без AI.
            # Оставлю как есть – заметил недочёт. Давай полностью переделаем ручной режим:
        if auto_mode:
            next_dir = snake.get_next_direction()
            game_over = not snake.move(next_dir)
        else:
            # Ручное управление с постоянным движением
            keys = pygame.key.get_pressed()
            new_dir = None
            if keys[pygame.K_UP]:
                new_dir = 0
            elif keys[pygame.K_RIGHT]:
                new_dir = 1
            elif keys[pygame.K_DOWN]:
                new_dir = 2
            elif keys[pygame.K_LEFT]:
                new_dir = 3
            if new_dir is not None:
                # Проверяем, не противоположное ли направление
                if (new_dir == 0 and snake.direction != 2) or \
                        (new_dir == 1 and snake.direction != 3) or \
                        (new_dir == 2 and snake.direction != 0) or \
                        (new_dir == 3 and snake.direction != 1):
                    snake.direction = new_dir
            game_over = not snake.move(snake.direction)

    # Отрисовка
    screen.fill(BLACK)
    for i, (x, y) in enumerate(snake.body):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    if snake.food:
        pygame.draw.rect(screen, RED,
                         (snake.food[1] * CELL_SIZE, snake.food[0] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    # Счет
    score_text = font.render(f"Score: {snake.score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    mode_text = font.render(f"Mode: {'AI' if auto_mode else 'Manual (arrows)'}", True, WHITE)
    screen.blit(mode_text, (10, HEIGHT - 30))
    if game_over:
        go_text = font.render("GAME OVER - Press R to restart", True, WHITE)
        screen.blit(go_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()
    clock.tick(10)  # скорость змейки (кадров в секунду)

pygame.quit()
sys.exit()