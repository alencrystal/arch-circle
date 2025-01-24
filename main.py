import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH = 800 # Dimensioni della finestra di gioco
WINDOW_HEIGHT = 600

GREEN = (35, 101, 51)           #player
BLACK = (0, 0, 0)               #sfondo
RED = (255, 0, 0)               #nemici
WHITE = (255, 255, 255)        #scritte
LIGHT_GREEN = (144, 238, 144)  #barra della vita

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Imposta la finestra di gioco
pygame.display.set_caption("arch-circle")

default_radius = 20 # Impostazioni del cerchio verde (giocatore)
circle_x = WINDOW_WIDTH // 2
circle_y = WINDOW_HEIGHT // 2
circle_speed = 5

player_health = 10 # Punti vita del giocatore
max_health = 10
health_bar_width = 50
health_bar_height = 5
player_attack = 1  # Danno del giocatore per colpo

# Impostazioni per i nemici
enemy_radius = 10
red_enemy_speed = 1.5  
spawn_timer = 0
spawn_interval = 1000  
min_spawn_interval = 200  
spawn_delay_timer = 0
time_still = 0  
enemies = []
blue_enemy_hp = 2  # HP dei nemici blu
blue_enemy_speed = 1.0  # Velocità dei nemici blu (più lenti dei rossi)


# Proiettili
bullet_radius = 5   
bullet_speed = 5 
bullet_timer = 0
bullet_interval = 980  
bullets = []

score = 0
experience = 0
enemies_killed = 0  # Contatore dei nemici uccisi per il prossimo "Level Up"

show_ui = False  # Di default, l'interfaccia è nascosta

font_small = pygame.font.Font(None, 36)

font = pygame.font.Font(None, 74) # Font per il messaggio di game over

clock = pygame.time.Clock()

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

    # Decidi casualmente se è un nemico blu o rosso (es. 20% blu, 80% rosso)
    if random.random() < 0.05:  # 20% di probabilità per il nemico blu
        enemies.append({"x": x, "y": y, "type": "blue", "hp": blue_enemy_hp})
    else:
        enemies.append({"x": x, "y": y, "type": "red"})



def get_closest_enemy():
    if not enemies:
        return None
    return min(enemies, key=lambda e: ((e["x"] - circle_x) ** 2 + (e["y"] - circle_y) ** 2))

def check_bullet_collision(bullet, enemy):
    # Calcola il vettore di spostamento del proiettile
    prev_x = bullet["x"] - bullet["dx"] * bullet_speed
    prev_y = bullet["y"] - bullet["dy"] * bullet_speed

    # Calcola la distanza minima tra la traiettoria del proiettile e il nemico
    enemy_pos = pygame.math.Vector2(enemy["x"], enemy["y"])
    bullet_start = pygame.math.Vector2(prev_x, prev_y)
    bullet_end = pygame.math.Vector2(bullet["x"], bullet["y"])
    distance_to_enemy = enemy_pos.distance_to(bullet_start)
    
    # Controlla se la traiettoria attraversa il nemico
    distance = enemy_pos.distance_to(bullet_end)
    return distance_to_enemy < bullet_radius + enemy_radius or distance < bullet_radius + enemy_radius


def game_over_screen():
    global score, circle_x, circle_y, player_health, enemies, bullets, time_still, spawn_interval

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:

                # Resett del gioco
                circle_x = WINDOW_WIDTH // 2
                circle_y = WINDOW_HEIGHT // 2
                player_health = max_health
                enemies = []
                bullets = []
                time_still = 0
                spawn_interval = 1000
                score = 0  # Resetta il punteggio
                return

        
        screen.fill(BLACK) 
        game_over_text = font.render("GAME OVER", True, WHITE)
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        restart_text = font_small.render("Press 'R' to Restart", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()


while True:                                 # Loop principale del gioco
    for event in pygame.event.get():
        enemies = [e for e in enemies if "type" in e]  # Rimuove eventuali nemici malformati

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            show_ui = not show_ui  # Alterna la visibilità dell'interfaccia


    
    keys = pygame.key.get_pressed()         # Ottieni gli input da tastiera
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

    
    if not moving:
        spawn_delay_timer += clock.get_time() / 1000  # Incrementa il tempo fermo
        if spawn_delay_timer >= 3:  # Dopo 3 secondi
            time_still += clock.get_time() / 1000  # Tempo in secondi
            spawn_interval = max(1000 - int(time_still * 80), min_spawn_interval)
    else:
        time_still = 0
        spawn_delay_timer = 0
        spawn_interval = 1000


    spawn_timer += clock.get_time()                         # Controlla il timer per spawnare i nemici
    if spawn_timer > spawn_interval:
        spawn_enemy()
        spawn_timer = 0

  
    bullet_timer += clock.get_time()                      # Controlla il timer per sparare proiettili
    if bullet_timer > bullet_interval and not moving:
        closest_enemy = get_closest_enemy()
        if closest_enemy:
            dx = closest_enemy["x"] - circle_x
            dy = closest_enemy["y"] - circle_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            bullets.append({"x": circle_x, "y": circle_y, "dx": dx / distance, "dy": dy / distance})
        bullet_timer = 0

 
    for enemy in enemies[:]:
        dx = circle_x - enemy["x"]
        dy = circle_y - enemy["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        speed = blue_enemy_speed if enemy["type"] == "blue" else red_enemy_speed

        if distance != 0:
            enemy["x"] += (dx / distance) * speed
            enemy["y"] += (dy / distance) * speed

        # Controllo della collisione con il giocatore
        if distance < default_radius + enemy_radius:
            player_health -= 1
            enemies.remove(enemy)
            continue

        for bullet in bullets[:]:
            bullet["x"] += bullet["dx"] * bullet_speed
            bullet["y"] += bullet["dy"] * bullet_speed

            # Rimuovi i proiettili fuori dallo schermo
            if bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT:
                bullets.remove(bullet)





    # Controlla collisione con il giocatore
        if distance < default_radius + enemy_radius:
            player_health -= 1
            enemies.remove(enemy)


    
    for bullet in bullets[:]:
        hit = False
        for enemy in enemies[:]:
            if check_bullet_collision(bullet, enemy):
                # Collisione rilevata, gestisci come prima
                if enemy["type"] == "blue":
                    enemy["hp"] -= player_attack
                    if enemy["hp"] <= 0:
                        enemies.remove(enemy)
                        score += 3  # 3 punti per i nemici blu
                        experience += 1  # Guadagna 1 punto esperienza per nemici rossi
                        enemies_killed += 1
                else:
                    enemies.remove(enemy)
                    score += 1
                    experience += 1  # Guadagna 1 punto esperienza per nemici rossi
                    enemies_killed += 1
                hit = True
                break
        if hit:
            bullets.remove(bullet)



    # Controlla se è necessario un Level Up
    if enemies_killed >= 15:
        enemies_killed = 0  # Resetta il contatore per il prossimo Level Up
        player_health = min(max_health, player_health + 2)  # Cura di 2 punti, senza superare il massimo
        max_health += 1  # Incrementa gli HP massimi di 1
        
        # Mostra il messaggio "Level Up"
        level_up_text = font.render("LEVEL UP!", True, WHITE)
        level_up_rect = level_up_text.get_rect(center=(circle_x, circle_y - default_radius - 30))

        # Pausa momentanea del gioco
        pause_timer = pygame.time.get_ticks()
        pause_duration = 1500 
        while pygame.time.get_ticks() - pause_timer < pause_duration:
            screen.fill(BLACK)
            pygame.draw.circle(screen, GREEN, (circle_x, circle_y), default_radius)  # Disegna il personaggio
            screen.blit(level_up_text, level_up_rect)  # Disegna "Level Up"
            
            # Disegna il punteggio e la barra della salute
            score_text = font_small.render(f"Score: {score}", True, WHITE)
            exp_text = font_small.render(f"EXP: {experience}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(exp_text, (10, 50))
            
            # Disegna nemici e proiettili per evitare un cambiamento brusco
            for enemy in enemies:
                color = RED if enemy["type"] == "red" else (0, 0, 255)
                pygame.draw.circle(screen, color, (int(enemy["x"]), int(enemy["y"])), enemy_radius)
            for bullet in bullets:
                pygame.draw.circle(screen, WHITE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)

            pygame.display.flip()



    if player_health <= 0:
        game_over_screen()


    screen.fill(BLACK)                                  # Disegna lo sfondo

    pygame.draw.circle(screen, GREEN, (circle_x, circle_y), default_radius)         # Disegna il cerchio verde

    for enemy in enemies:
        color = RED if enemy["type"] == "red" else (0, 0, 255)  # Blu per i nemici blu
        pygame.draw.circle(screen, color, (int(enemy["x"]), int(enemy["y"])), enemy_radius)



    for bullet in bullets:                                                                       # Disegna i proiettili
        pygame.draw.circle(screen, WHITE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)


    health_ratio = player_health / max_health                                                           # Disegna la barra della vita
    current_health_bar_width = int(health_bar_width * health_ratio)
    pygame.draw.rect(screen, RED, (circle_x - health_bar_width // 2, circle_y + default_radius + 10, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, LIGHT_GREEN, (circle_x - health_bar_width // 2, circle_y + default_radius + 10, current_health_bar_width, health_bar_height))

    score_text = font_small.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

    if show_ui:
        hp_text = font_small.render(f"HP: {player_health}/{max_health}", True, WHITE)
        screen.blit(hp_text, (10, 10))  # Posiziona il testo nella UI
        
        # Disegna l'EXP
        exp_text = font_small.render(f"exp: {experience}", True, WHITE)
        screen.blit(exp_text, (10, 50))
        
        # Disegna l'intervallo di spawn
        spawn_text = font_small.render(f"si: {spawn_interval}", True, WHITE)
        screen.blit(spawn_text, (10, 90))


    pygame.display.flip()                                                                               # Aggiorna la finestra
    clock.tick(60)                                                                                       # Limita il frame rate a 60 FPS
