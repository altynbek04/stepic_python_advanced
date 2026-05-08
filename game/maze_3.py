import pygame
import random
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cave Escape - бесконечный раннер")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Игрок
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_X = 100
player_y = HEIGHT - PLAYER_HEIGHT - 20
player_vel_y = 0
gravity = 0.8
jump_power = -12
is_crouching = False
normal_height = PLAYER_HEIGHT
crouch_height = 18

# Препятствия (шипы)
spikes = []  # каждый шип: pygame.Rect(x, y, width, height), тип "top" или "bottom"
SPIKE_WIDTH = 25
SPIKE_HEIGHT = 15
spawn_timer = 0
spawn_delay = 90  # кадров между появлением

# Монеты
coins = []
COIN_SIZE = 15
coin_spawn_timer = 0
coin_delay = 120

# Параметры мира
scroll_speed = 6
score = 0
game_over = False
auto_mode = False  # False - ручной, True - AI


# --- Функция AI (примитивный бот) ---
def ai_decision(player_y, player_height, nearest_spike):
    """
    nearest_spike: {'rect': Rect, 'type': 'top' or 'bottom'}
    Возвращает True если нужно прыгнуть, False если присесть, None если ничего.
    """
    if not nearest_spike:
        return None

    spike_rect = nearest_spike['rect']
    spike_type = nearest_spike['type']
    distance = spike_rect.x - PLAYER_X

    if distance > 80:  # слишком далеко
        return None
    if distance < -20:  # уже позади
        return None

    if spike_type == 'top':
        # шип сверху -> нужно присесть, если он низко
        if spike_rect.bottom > player_y + player_height - 10:
            return 'crouch'
        else:
            return None
    else:  # 'bottom' шип снизу
        # нужно прыгнуть, если шип высоко
        if spike_rect.top < player_y + player_height - 10:
            return 'jump'
        else:
            return None


# --- Генерация препятствия ---
def spawn_spike():
    spike_type = random.choice(['top', 'bottom'])
    if spike_type == 'top':
        y = 0
        rect = pygame.Rect(WIDTH, y, SPIKE_WIDTH, SPIKE_HEIGHT)
    else:
        y = HEIGHT - SPIKE_HEIGHT
        rect = pygame.Rect(WIDTH, y, SPIKE_WIDTH, SPIKE_HEIGHT)
    spikes.append({'rect': rect, 'type': spike_type})


# --- Генерация монеты ---
def spawn_coin():
    y = random.randint(50, HEIGHT - 70)
    coins.append(pygame.Rect(WIDTH, y, COIN_SIZE, COIN_SIZE))


# --- Функция перезапуска ---
def reset_game():
    global player_y, player_vel_y, is_crouching, spikes, coins, score, game_over, spawn_timer, coin_spawn_timer
    player_y = HEIGHT - PLAYER_HEIGHT - 20
    player_vel_y = 0
    is_crouching = False
    spikes.clear()
    coins.clear()
    score = 0
    game_over = False
    spawn_timer = 0
    coin_spawn_timer = 0


# --- Основной цикл ---
reset_game()
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # нажми M, чтобы переключить режим (Manual/Auto)
                    auto_mode = not auto_mode
                    print(f"Режим: {'AUTO (AI играет)' if auto_mode else 'MANUAL (ты играешь)'}")

    if not game_over:
        # --- Управление (ручное или AI) ---
        if auto_mode:
            # Найти ближайший шип впереди
            nearest = None
            for s in spikes:
                if s['rect'].x + SPIKE_WIDTH > PLAYER_X:
                    nearest = s
                    break
            action = ai_decision(player_y, normal_height if not is_crouching else crouch_height, nearest)
            if action == 'jump' and not is_crouching and player_vel_y == 0:
                player_vel_y = jump_power
            elif action == 'crouch':
                is_crouching = True
            else:
                # Если не прыгаем и не приседаем, то встаём
                is_crouching = False
        else:
            # Ручное управление
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not is_crouching and player_vel_y == 0:
                player_vel_y = jump_power
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                is_crouching = True
            else:
                is_crouching = False

        # Физика прыжка
        player_vel_y += gravity
        player_y += player_vel_y
        # Гравитация и пол
        ground_y = HEIGHT - (crouch_height if is_crouching else normal_height) - 20
        if player_y > ground_y:
            player_y = ground_y
            player_vel_y = 0

        # Сдвиг мира (движение препятствий и монет)
        for s in spikes:
            s['rect'].x -= scroll_speed
        spikes = [s for s in spikes if s['rect'].x + SPIKE_WIDTH > 0]

        for c in coins[:]:
            c.x -= scroll_speed
            if c.x + COIN_SIZE < 0:
                coins.remove(c)

        # Спавн новых препятствий
        if spawn_timer <= 0:
            spawn_spike()
            spawn_timer = spawn_delay
        else:
            spawn_timer -= 1

        # Спавн монет
        if coin_spawn_timer <= 0:
            spawn_coin()
            coin_spawn_timer = coin_delay
        else:
            coin_spawn_timer -= 1

        # Проверка столкновений с шипами
        current_height = crouch_height if is_crouching else normal_height
        player_rect = pygame.Rect(PLAYER_X, player_y, PLAYER_WIDTH, current_height)
        for s in spikes:
            if player_rect.colliderect(s['rect']):
                game_over = True
                break

        # Сбор монет
        for c in coins[:]:
            if player_rect.colliderect(c):
                coins.remove(c)
                score += 1

        # --- Отрисовка ---
        # Игрок
        pygame.draw.rect(screen, GREEN, (PLAYER_X, player_y, PLAYER_WIDTH, current_height))
        # Шипы
        for s in spikes:
            pygame.draw.rect(screen, RED, s['rect'])
        # Монеты
        for c in coins:
            pygame.draw.circle(screen, YELLOW, (c.x + COIN_SIZE // 2, c.y + COIN_SIZE // 2), COIN_SIZE // 2)
    else:
        # Экран Game Over
        go_text = font.render("GAME OVER", True, RED)
        screen.blit(go_text, (WIDTH // 2 - 70, HEIGHT // 2 - 40))
        score_text = font.render(f"Счёт: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - 40, HEIGHT // 2))
        restart_text = font.render("Нажми R для новой игры", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 40))
        mode_text = font.render(f"Режим: {'AUTO' if auto_mode else 'MANUAL'}", True, GRAY)
        screen.blit(mode_text, (WIDTH // 2 - 80, HEIGHT // 2 + 80))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()

    # Отображение счёта и режима
    if not game_over:
        score_surf = font.render(f"Монеты: {score}", True, BLACK)
        screen.blit(score_surf, (10, 10))
        mode_surf = font.render(f"Режим: {'AI' if auto_mode else 'Игрок'}", True, BLACK)
        screen.blit(mode_surf, (WIDTH - 150, 10))
        hint = font.render("M - сменить режим", True, GRAY)
        screen.blit(hint, (10, HEIGHT - 30))
        if not auto_mode:
            controls = font.render("Пробел - прыжок, Shift - присесть", True, GRAY)
            screen.blit(controls, (10, HEIGHT - 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()