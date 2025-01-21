import pygame
import sys
import random

# Inizializza Pygame
pygame.init()

# Dimensioni della finestra di gioco
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colori
GREEN = (35, 101, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)  # Colore più chiaro per la barra della vita

# Imposta la finestra di gioco
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gioco del Cerchio Verde")

# Impostazioni del cerchio verde (giocatore)
default_radius = 20
circle_x = WINDOW_WIDTH // 2
circle_y = WINDOW_HEIGHT // 2
circle_speed = 5

# Punti vita del giocatore
player_health = 10
max_health = 10
health_bar_width = 50
health_bar_height = 5

# Impostazioni per i nemici
enemy_radius = 10
enemy_speed = 1.5  # Nemici più lenti
spawn_timer = 0
spawn_interval = 1000  # Millisecondi
min_spawn_interval = 200  # Minimo intervallo di spawn
spawn_delay_timer = 0  # Ritardo per iniziare a diminuire lo spawn interval
time_still = 0  # Tempo totale in cui il giocatore è rimasto fermo
enemies = []

# Proiettili
bullet_radius = 5
bullet_speed = 7
bullet_timer = 0
bullet_interval = 1000  # 1 secondo tra un proiettile e l'altro
bullets = []

# Punteggio
score = 0
font_small = pygame.font.Font(None, 36)

# Font per il messaggio di game over
font = pygame.font.Font(None, 74)

# Clock per controllare il frame rate
clock = pygame.time.Clock()

# Funzione per gestire i nemici
def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, WINDOW_WIDTH)
        y = 0
    elif side == "bottom":
        x = random.randint(0, WINDOW_WIDTH)
        y = WINDOW_HEIGHT
    elif side == "left":
        x = 0
        y = random.randint(0, WINDOW_HEIGHT)
    elif side == "right":
        x = WINDOW_WIDTH
        y = random.randint(0, WINDOW_HEIGHT)

    enemies.append({"x": x, "y": y})

# Funzione per calcolare il nemico più vicino

def get_closest_enemy():
    if not enemies:
        return None
    return min(enemies, key=lambda e: ((e["x"] - circle_x) ** 2 + (e["y"] - circle_y) ** 2))

# Loop principale del gioco
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ottieni gli input da tastiera
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_UP] and circle_y - default_radius > 0:
        circle_y -= circle_speed
        moving = True
    if keys[pygame.K_DOWN] and circle_y + default_radius < WINDOW_HEIGHT:
        circle_y += circle_speed
        moving = True
    if keys[pygame.K_LEFT] and circle_x - default_radius > 0:
        circle_x -= circle_speed
        moving = True
    if keys[pygame.K_RIGHT] and circle_x + default_radius < WINDOW_WIDTH:
        circle_x += circle_speed
        moving = True

    # Controlla se il giocatore è fermo
    if not moving:
        spawn_delay_timer += clock.get_time() / 1000  # Incrementa il tempo fermo
        if spawn_delay_timer >= 3:  # Dopo 3 secondi
            time_still += clock.get_time() / 1000  # Tempo in secondi
            spawn_interval = max(1000 - int(time_still * 80), min_spawn_interval)
    else:
        time_still = 0
        spawn_delay_timer = 0
        spawn_interval = 1000

    # Controlla il timer per spawnare i nemici
    spawn_timer += clock.get_time()
    if spawn_timer > spawn_interval:
        spawn_enemy()
        spawn_timer = 0

    # Controlla il timer per sparare proiettili
    bullet_timer += clock.get_time()
    if bullet_timer > bullet_interval and not moving:
        closest_enemy = get_closest_enemy()
        if closest_enemy:
            dx = closest_enemy["x"] - circle_x
            dy = closest_enemy["y"] - circle_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            bullets.append({"x": circle_x, "y": circle_y, "dx": dx / distance, "dy": dy / distance})
        bullet_timer = 0

    # Muovi i nemici e controlla le collisioni
    for enemy in enemies[:]:
        dx = circle_x - enemy["x"]
        dy = circle_y - enemy["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        enemy["x"] += (dx / distance) * enemy_speed
        enemy["y"] += (dy / distance) * enemy_speed

        # Controlla la collisione con il giocatore
        if distance < default_radius + enemy_radius:
            player_health -= 1
            enemies.remove(enemy)

    # Muovi i proiettili e controlla le collisioni con i nemici
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"] * bullet_speed
        bullet["y"] += bullet["dy"] * bullet_speed

        # Rimuovi il proiettile se esce dallo schermo
        if (bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or
            bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT):
            bullets.remove(bullet)
            continue

        # Controlla la collisione con i nemici
        for enemy in enemies[:]:
            distance = ((bullet["x"] - enemy["x"]) ** 2 + (bullet["y"] - enemy["y"]) ** 2) ** 0.5
            if distance < bullet_radius + enemy_radius:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    if player_health <= 0:
        # Mostra il messaggio di Game Over
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Disegna lo sfondo
    screen.fill(BLACK)

    # Disegna il cerchio verde
    pygame.draw.circle(screen, GREEN, (circle_x, circle_y), default_radius)

    # Disegna i nemici
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (int(enemy["x"]), int(enemy["y"])), enemy_radius)

    # Disegna i proiettili
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)

    # Disegna la barra della vita
    health_ratio = player_health / max_health
    current_health_bar_width = int(health_bar_width * health_ratio)
    pygame.draw.rect(screen, RED, (circle_x - health_bar_width // 2, circle_y + default_radius + 10, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, LIGHT_GREEN, (circle_x - health_bar_width // 2, circle_y + default_radius + 10, current_health_bar_width, health_bar_height))

    # Disegna il punteggio
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Disegna l'intervallo di spawn
    spawn_text = font_small.render(f"S.P.: {spawn_interval}", True, WHITE)
    screen.blit(spawn_text, (WINDOW_WIDTH - 150, 10))

    # Aggiorna la finestra
    pygame.display.flip()

    # Limita il frame rate a 60 FPS
    clock.tick(60)
