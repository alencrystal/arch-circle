import pygame
import sys
import random

pygame.init()

background = pygame.image.load("images/floor_wood.jpg")  # Sostituisci con il nome del tuo file


WINDOW_WIDTH =  700 # Dimensioni della finestra di gioco
WINDOW_HEIGHT = 700


background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

GREEN = (35, 101, 51)           
BLACK = (0, 0, 0)               
RED = (255, 0, 0)               
WHITE = (255, 255, 255)        
LIGHT_GREEN = (144, 238, 144)  
YELLOW = (222, 208, 108)   

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

spawn_timer = 0
spawn_interval = 1000  
min_spawn_interval = 200  
spawn_delay_timer = 0
time_still = 0  
enemies = []


#nemici rossi
red_enemy_speed = 1.5
enemy_radius = 10 

#nemici blu
blue_enemy_hp = 2  
blue_enemy_speed = 1  

#nemici neri
black_enemy_hp = 5  
black_enemy_speed = 0.8  
black_enemy_radius = 15 

 


# Proiettili
bullet_radius = 5   
bullet_speed = 7 
bullet_timer = 0
bullet_interval = 1000  
bullets = []

score = 0
experience = 0
enemies_killed = 0  

show_ui = False  # Di default, l'interfaccia è nascosta

font_small = pygame.font.Font("font/Titillium.ttf", 30)

font = pygame.font.Font("font/Titillium.ttf", 74) # Font per il messaggio di game over

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

    rand = random.random()

    #10% possibilità di spawn
    if rand < 0.10:  
        enemies.append({"x": x, "y": y, "type": "blue", "hp": blue_enemy_hp})

    #5% possibilità di spawn
    elif rand < 0.15:  
        enemies.append({"x": x, "y": y, "type": "black", "hp": black_enemy_hp})
    
    #resto dello spawn 
    else:
        enemies.append({"x": x, "y": y, "type": "red"})


def get_closest_enemy():
    if not enemies:
        return None
    return min(enemies, key=lambda e: ((e["x"] - circle_x) ** 2 + (e["y"] - circle_y) ** 2))

def check_bullet_collision(bullet, enemy):
    # Versione semplificata per collisioni affidabili
    dx = bullet["x"] - enemy["x"]
    dy = bullet["y"] - enemy["y"]
    return (dx**2 + dy**2) ** 0.5 < (bullet_radius + enemy_radius)

def game_over_screen():
    global score, circle_x, circle_y, player_health, max_health, enemies, bullets, time_still, spawn_interval, enemies_killed, experience, bullet_interval

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset completo di tutti i valori
                circle_x = WINDOW_WIDTH // 2
                circle_y = WINDOW_HEIGHT // 2
                max_health = 10  # Resetta gli HP massimi
                player_health = max_health
                
                enemies = []
                bullets = []
                time_still = 0
                spawn_interval = 1000
                
                score = 0
                enemies_killed = 0
                bullet_interval = 980
                experience = 0    
                
                return

        screen.blit(background, (0, 0))
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

def level_up_menu():
    global player_health, max_health, bullet_interval, spawn_interval, spawn_delay_timer, score

    # Configura i buff
    buffs = [
        {"name": "Heal", "action": lambda: heal_player(5)},  # Cura
        {"name": "Max HP", "action": lambda: increase_max_health(2)},  # Incremento salute massima
        {"name": "Faster Reload", "action": lambda: reduce_bullet_interval(50)},  # Riduzione bullet_interval
    ]

    # Disegna i tre buff come rettangoli
    options_rects = []
    for i, buff in enumerate(buffs):
        rect = pygame.Rect((WINDOW_WIDTH // 4 * (i + 1) - 50, WINDOW_HEIGHT // 2 - 50, 100, 100))
        options_rects.append(rect)

    selected_option = 0  # Tiene traccia dell'opzione selezionata

    # Mostra il menu finché non si sceglie un buff
    while True:
        screen.blit(background, (0, 0))

        # Disegna la scritta "Level Up" in alto al centro
        level_up_text = font.render("LEVEL UP!", True, WHITE)
        level_up_rect = level_up_text.get_rect(center=(WINDOW_WIDTH // 2, 100))  # Posiziona in alto
        screen.blit(level_up_text, level_up_rect)

        # Disegna i rettangoli con i nomi dei buff
        for i, rect in enumerate(options_rects):
            color = LIGHT_GREEN if i == selected_option else YELLOW  # Cambia il colore in base alla selezione
            pygame.draw.rect(screen, color, rect)
            buff_text = font_small.render(buffs[i]["name"], True, WHITE)
            text_rect = buff_text.get_rect(center=rect.center)
            screen.blit(buff_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(buffs)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(buffs)
                elif event.key == pygame.K_RETURN:  # Invio per confermare la selezione
                    buffs[selected_option]["action"]()
                    score += player_health  # Aggiungi gli HP attuali al punteggio
                    spawn_delay_timer = 0  # Resetta il timer di inattività
                    spawn_interval = 1000  # Torna al valore iniziale dello spawn interval
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Click sinistro
                for i, rect in enumerate(options_rects):
                    if rect.collidepoint(event.pos):
                        buffs[i]["action"]()
                        score += player_health  # Aggiungi gli HP attuali al punteggio
                        spawn_delay_timer = 0  # Resetta il timer di inattività
                        spawn_interval = 1000  # Torna al valore iniziale dello spawn interval 
                        return



def heal_player(amount):
    global player_health, max_health
    player_health = max_health  # Cura fino al massimo

def increase_max_health(amount):
    global player_health, max_health
    max_health += amount
    player_health += amount
    

def reduce_bullet_interval(amount):
    global bullet_interval
    bullet_interval = max(200, bullet_interval - amount)  # Limita il bullet_interval minimo


# ============================================================
# MAIN GAME LOOP
# ============================================================
while True:
    for event in pygame.event.get():
        enemies = [e for e in enemies if "type" in e]

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            show_ui = not show_ui

    # Movimento giocatore
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

    # Logica spawn nemici
    if not moving:
        spawn_delay_timer += clock.get_time() / 1000
        if spawn_delay_timer >= 3:
            time_still += clock.get_time() / 1000
            spawn_interval = max(1000 - int(time_still * 80), min_spawn_interval)
    else:
        time_still = 0
        spawn_delay_timer = 0
        spawn_interval = 1000

    spawn_timer += clock.get_time()
    if spawn_timer > spawn_interval:
        spawn_enemy()
        spawn_timer = 0

    # Sparare proiettili
    bullet_timer += clock.get_time()
    if bullet_timer > bullet_interval and not moving:
        closest_enemy = get_closest_enemy()
        if closest_enemy:
            dx = closest_enemy["x"] - circle_x
            dy = closest_enemy["y"] - circle_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 0:  # Previene divisione per zero
                bullets.append({"x": circle_x, "y": circle_y, "dx": dx/distance, "dy": dy/distance})
        bullet_timer = 0

    # Muovi prima TUTTI i proiettili
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"] * bullet_speed
        bullet["y"] += bullet["dy"] * bullet_speed
        # Rimuovi proiettili fuori dallo schermo
        if bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT:
            bullets.remove(bullet)

    # Movimento e collisioni nemici
    for enemy in enemies[:]:
        dx = circle_x - enemy["x"]
        dy = circle_y - enemy["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if enemy["type"] == "blue":
            speed = blue_enemy_speed
        elif enemy["type"] == "black":
            speed = black_enemy_speed
        else:
            speed = red_enemy_speed


        if distance != 0:
            enemy["x"] += (dx / distance) * speed
            enemy["y"] += (dy / distance) * speed

        # Collisione con il giocatore
        if distance < default_radius + enemy_radius:
            player_health -= 1
            enemies.remove(enemy)

    # Controllo collisioni proiettili DOPO averli mossi
    for bullet in bullets[:]:
        hit = False
        for enemy in enemies[:]:
            if check_bullet_collision(bullet, enemy):
                if enemy["type"] == "blue" or enemy["type"] == "black":
                    enemy["hp"] -= player_attack
                    if enemy["hp"] <= 0:
                        if enemy["type"] == "black":
                            # Quando il nemico nero muore, genera 2 nemici rossi affiancati
                            offset = enemy_radius + 5  # Distanza tra i due nuovi nemici
                            enemies.append({"x": enemy["x"] - offset, "y": enemy["y"], "type": "red"})
                            enemies.append({"x": enemy["x"] + offset, "y": enemy["y"], "type": "red"})

                            score += 9  # Il nemico nero dà più punti
                            experience += 1
                            enemies_killed += 1
                        else:
                            score += 3  # Il nemico blu dà 3 punti
                            experience += 1
                            enemies_killed += 1
                        enemies.remove(enemy)
                else:
                    enemies.remove(enemy)
                    score += 1
                    experience += 1
                    enemies_killed += 1


                
                hit = True
                break  # Esci dal loop dopo la prima collisione
        if hit:
            bullets.remove(bullet)

    




    # Level Up system
    if enemies_killed >= 15:
        enemies_killed = 0
        level_up_menu()  # Mostra il menu per la scelta del buff
        
        

        
    if player_health <= 0:
        game_over_screen()

    # Disegno elementi
    screen.blit(background, (0, 0))

    # Disegna il bordo nero (cerchio leggermente più grande)
    pygame.draw.circle(screen, BLACK, (circle_x, circle_y), default_radius + 2)

    # Disegna il player sopra il bordo
    pygame.draw.circle(screen, GREEN, (circle_x, circle_y), default_radius)


    for enemy in enemies:
        if enemy["type"] == "red":
            color = RED
            radius = enemy_radius
        elif enemy["type"] == "blue":
            color = (0, 0, 255)
            radius = enemy_radius
        else:  # Nemico nero
            color = BLACK
            radius = black_enemy_radius

        # Disegna il bordo nero e poi il nemico
        pygame.draw.circle(screen, BLACK, (int(enemy["x"]), int(enemy["y"])), radius + 2)
        pygame.draw.circle(screen, color, (int(enemy["x"]), int(enemy["y"])), radius)



    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)

    # UI
    health_ratio = player_health / max_health
    current_health_bar_width = int(health_bar_width * health_ratio)
    pygame.draw.rect(screen, RED, (circle_x - health_bar_width//2, circle_y + default_radius + 10, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, LIGHT_GREEN, (circle_x - health_bar_width//2, circle_y + default_radius + 10, current_health_bar_width, health_bar_height))

    score_text = font_small.render(f"{score}", True, WHITE)  # Mostra solo il numero
    score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))  # Allineato a destra
    screen.blit(score_text, score_rect)


    if show_ui:

        ui_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        
        # Posiziona il pannello in alto a sinistra
        screen.blit(ui_surface, (0, 0))  
        
        # Disegna i testi SOPRA il pannello
        hp_text = font_small.render(f"HP: {player_health}/{max_health}", True, WHITE)
        exp_text = font_small.render(f"EXP: {experience}", True, WHITE)
        spawn_text = font_small.render(f"SI: {spawn_interval}", True, WHITE)
        bullet_text = font_small.render(f"AS: {bullet_interval}", True, WHITE)
        
        screen.blit(hp_text, (10, 10))    
        screen.blit(exp_text, (10, 50))   
        screen.blit(spawn_text, (10, 90)) 
        screen.blit(bullet_text, (10, 130)) 

    pygame.display.flip()
    clock.tick(60)

#eskere
#puwh2 amogus