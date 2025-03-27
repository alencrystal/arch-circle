#!/bin/bash

# Crea la directory principale
mkdir arch-circle
cd arch-circle

# Crea i file Python
touch main.py enemy.py player.py bullet.py ui.py game.py config.py utils.py

# Crea la directory assets e le sottodirectory
mkdir -p assets/images assets/font

# Aggiungi placeholder per gli asset (sostituisci con i tuoi file)
touch assets/images/tile_floor_wood.jpg
touch assets/font/Titillium.ttf
echo "Placeholder image" > assets/images/tile_floor_wood.jpg  # Placeholder testuale, se necessario
echo "Placeholder font" > assets/font/Titillium.ttf   # Placeholder testuale



# Inserisci il codice Python nei file (usa 'cat' e l'heredoc)

cat << EOF > config.py
# config.py
import pygame

pygame.init()

# Dimensioni finestra
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

# Colori
GREEN = (35, 101, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
YELLOW = (222, 208, 108)

# Font
FONT_SMALL = pygame.font.Font("assets/font/Titillium.ttf", 30)
FONT_LARGE = pygame.font.Font("assets/font/Titillium.ttf", 74)

# Player settings (potrebbero essere spostate in player.py se diventano troppo specifiche)
DEFAULT_RADIUS = 20
PLAYER_SPEED = 5
PLAYER_INITIAL_HEALTH = 10
PLAYER_ATTACK = 1

# Enemy settings (potrebbero essere spostate in enemy.py)
RED_ENEMY_SPEED = 1.5
ENEMY_RADIUS = 10
BLUE_ENEMY_HP = 2
BLUE_ENEMY_SPEED = 1
BLACK_ENEMY_HP = 5
BLACK_ENEMY_SPEED = 0.8
BLACK_ENEMY_RADIUS = 15

# Bullet settings
BULLET_RADIUS = 5
BULLET_SPEED = 7

# Game settings
INITIAL_SPAWN_INTERVAL = 1000
MIN_SPAWN_INTERVAL = 200
INITIAL_BULLET_INTERVAL = 1000
EOF


cat << EOF > utils.py
# utils.py
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT

def random_spawn_position():
    """Genera una posizione casuale ai bordi dello schermo."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return random.randint(0, WINDOW_WIDTH), 0
    elif side == "bottom":
        return random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT
    elif side == "left":
        return 0, random.randint(0, WINDOW_HEIGHT)
    elif side == "right":
        return WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT)


def calculate_distance(pos1, pos2):
    """Calcola la distanza tra due punti (x, y)."""
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
EOF


cat << EOF > player.py
# player.py
import pygame
from config import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = DEFAULT_RADIUS
        self.speed = PLAYER_SPEED
        self.health = PLAYER_INITIAL_HEALTH
        self.max_health = PLAYER_INITIAL_HEALTH
        self.attack = PLAYER_ATTACK
        self.health_bar_width = 50  # Aggiunto per coerenza
        self.health_bar_height = 5  # Aggiunto

    def move(self, keys):
        """Gestisce il movimento del giocatore in base ai tasti premuti."""
        if keys[pygame.K_UP] and self.y - self.radius > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.radius < WINDOW_HEIGHT:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.radius < WINDOW_WIDTH:
            self.x += self.speed

    def draw(self, screen):
        """Disegna il giocatore e la barra della vita."""
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius + 2)
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

        # Barra della vita
        health_ratio = self.health / self.max_health
        current_health_bar_width = int(self.health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (self.x - self.health_bar_width // 2, self.y + self.radius + 10, self.health_bar_width, self.health_bar_height))
        pygame.draw.rect(screen, LIGHT_GREEN, (self.x - self.health_bar_width // 2, self.y + self.radius + 10, current_health_bar_width, self.health_bar_height))


    def is_colliding(self, enemy):
        """Controlla collisione con nemici."""
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance < self.radius + enemy.radius


    def take_damage(self, amount):
        """Gestisce danno."""
        self.health -= amount

    def heal(self, amount):
        """Aumenta gli HP (fino al massimo)."""
        self.health = min(self.max_health, self.health + amount)

    def increase_max_health(self, amount):
        """Incrementa la salute massima."""
        self.max_health += amount
        self.health += amount  # Opzionale: cura anche quando aumenti la salute massima
EOF

cat << EOF > enemy.py
# enemy.py
import pygame
from config import *
from utils import calculate_distance

class Enemy:
    def __init__(self, x, y, speed, color, radius, hp=1):  # hp come parametro opzionale
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.radius = radius
        self.hp = hp

    def move_towards(self, target_x, target_y):
        """Muove il nemico verso una posizione target."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = calculate_distance((self.x, self.y), (target_x, target_y))
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):
        """Disegna il nemico."""
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def take_damage(self, damage):
        """Gestisce il danno subito."""
        self.hp -= damage
        return self.hp <= 0  # Restituisce True se il nemico è morto

# Sottoclassi per tipi specifici di nemici
class RedEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, RED_ENEMY_SPEED, RED, ENEMY_RADIUS)

class BlueEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, BLUE_ENEMY_SPEED, (0, 0, 255), ENEMY_RADIUS, BLUE_ENEMY_HP)

class BlackEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, BLACK_ENEMY_SPEED, BLACK, BLACK_ENEMY_RADIUS, BLACK_ENEMY_HP)

    def spawn_red_enemies(self):
        """Genera due nemici rossi quando il nemico nero muore"""
        offset = self.radius + 5
        return [RedEnemy(self.x - offset, self.y), RedEnemy(self.x + offset, self.y)]
EOF

cat << EOF > bullet.py
# bullet.py
import pygame
from config import *

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS

    def move(self):
        """Muove il proiettile."""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, screen):
        """Disegna il proiettile."""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def is_offscreen(self):
        """Controlla se il proiettile è fuori dallo schermo"""
        return self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT
    
    def check_collision(self, enemy):
        """Controlla collisione proiettile."""
        dx = self.x - enemy.x
        dy = self.y - enemy.y
        return (dx**2 + dy**2) ** 0.5 < (self.radius + enemy.radius)
EOF

cat << EOF > ui.py
# ui.py
import pygame
from config import *

def draw_tiled_background(screen, background_image):
    """Disegna lo sfondo ripetuto."""
    for x in range(0, WINDOW_WIDTH, background_image.get_width()):
        for y in range(0, WINDOW_HEIGHT, background_image.get_height()):
            screen.blit(background_image, (x, y))

def draw_score(screen, score):
    """Disegna il punteggio."""
    score_text = FONT_SMALL.render(f"{score}", True, WHITE)
    score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

def draw_game_over_screen(screen, score):
    """Mostra la schermata di Game Over."""
    screen.fill(BLACK)  # Pulisce lo schermo, potresti anche usare draw_tiled_background

    game_over_text = FONT_LARGE.render("GAME OVER", True, WHITE)
    score_text = FONT_SMALL.render(f"Score: {score}", True, WHITE)
    restart_text = FONT_SMALL.render("Press 'R' to Restart", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def draw_level_up_menu(screen, buffs, selected_option):
    """Disegna il menu di level up e gestisce la selezione."""
    screen.fill(BLACK) # Pulisci schermo, oppure draw_tiled_background

    level_up_text = FONT_LARGE.render("LEVEL UP!", True, WHITE)
    level_up_rect = level_up_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(level_up_text, level_up_rect)

    options_rects = []
    for i, buff in enumerate(buffs):
        rect = pygame.Rect((WINDOW_WIDTH // 4 * (i + 1) - 50, WINDOW_HEIGHT // 2 - 50, 100, 100))
        options_rects.append(rect)
        color = LIGHT_GREEN if i == selected_option else YELLOW
        pygame.draw.rect(screen, color, rect)
        buff_text = FONT_SMALL.render(buffs[i]["name"], True, WHITE)
        text_rect = buff_text.get_rect(center=rect.center)
        screen.blit(buff_text, text_rect)

    pygame.display.flip()
    return options_rects  # Restituisci i rect per la gestione del click


def draw_ui(screen, player, experience, spawn_interval, bullet_interval, level):
    """Disegna tutti gli elementi della UI (se visibile)."""
    ui_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    screen.blit(ui_surface, (0, 0))

    hp_text = FONT_SMALL.render(f"HP: {player.health}/{player.max_health}", True, WHITE)
    exp_text = FONT_SMALL.render(f"EXP: {experience}", True, WHITE)
    spawn_text = FONT_SMALL.render(f"SI: {spawn_interval}", True, WHITE)
    bullet_text = FONT_SMALL.render(f"AS: {bullet_interval}", True, WHITE)
    level_text = FONT_SMALL.render(f"LV: {level}", True, WHITE)

    screen.blit(hp_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(exp_text, (10, 90))
    screen.blit(bullet_text, (10, 130))
    screen.blit(spawn_text, (10, 170))
EOF

cat << EOF > game.py
# game.py
import pygame
import sys
import random
from config import *
from player import Player
from enemy import RedEnemy, BlueEnemy, BlackEnemy
from bullet import Bullet
from ui import draw_tiled_background, draw_score, draw_game_over_screen, draw_level_up_menu, draw_ui
from utils import random_spawn_position, calculate_distance

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.experience = 0
        self.level = 1
        self.exp_to_next_level = 10
        self.spawn_timer = 0
        self.spawn_interval = INITIAL_SPAWN_INTERVAL
        self.min_spawn_interval = MIN_SPAWN_INTERVAL
        self.spawn_delay_timer = 0
        self.time_still = 0
        self.bullet_timer = 0
        self.bullet_interval = INITIAL_BULLET_INTERVAL
        self.running = True
        self.show_ui = False
        self.background = pygame.image.load("assets/images/tile_floor_wood.jpg")
        self.background = pygame.transform.scale(self.background, (256, 256))

    def handle_input(self):
        """Gestisce l'input dell'utente (tasti, mouse, ecc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.show_ui = not self.show_ui
                if event.key == pygame.K_r and self.player.health <= 0:  # Riavvia
                    self.reset_game()

    def update(self):
        """Aggiorna la logica di gioco (movimento, collisioni, ecc.)."""
        keys = pygame.key.get_pressed()
        moving = any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]])
        self.player.move(keys)

        # Spawn nemici
        self.update_spawn_logic(moving)

        # Sparo proiettili
        self.update_bullets(moving)

        # Movimento nemici e collisioni
        self.update_enemies()

        # Controllo collisioni proiettili
        self.check_bullet_collisions()
        
        # Level up
        self.check_level_up()

        # Game over
        if self.player.health <= 0:
            draw_game_over_screen(self.screen, self.score)
            

    def draw(self):
        """Disegna tutti gli elementi del gioco."""
        draw_tiled_background(self.screen, self.background)  # Usa la funzione da ui.py
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        draw_score(self.screen, self.score)  # Usa la funzione da ui.py
        if self.show_ui:
            draw_ui(self.screen, self.player, self.experience, self.spawn_interval, self.bullet_interval, self.level)


        pygame.display.flip()


    def run(self):
        """Ciclo principale del gioco."""
        while self.running:
            self.handle_input()
            if self.player.health > 0:  # Aggiorna solo se non è game over
                self.update()
            self.draw()
            self.clock.tick(60)

    def update_spawn_logic(self, moving):
        """Logica per lo spawn dei nemici."""
        if not moving:
            self.spawn_delay_timer += self.clock.get_time() / 1000
            if self.spawn_delay_timer >= 3:
                self.time_still += self.clock.get_time() / 1000
                self.spawn_interval = max(1000 - int(self.time_still * 80), self.min_spawn_interval)
        else:
            self.time_still = 0
            self.spawn_delay_timer = 0
            self.spawn_interval = 1000

        self.spawn_timer += self.clock.get_time()
        if self.spawn_timer > self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0

    def spawn_enemy(self):
        """Genera un nemico casuale."""
        x, y = random_spawn_position()
        rand = random.random()
        if rand < 0.10:
            self.enemies.append(BlueEnemy(x, y))
        elif rand < 0.15:
            self.enemies.append(BlackEnemy(x, y))
        else:
            self.enemies.append(RedEnemy(x, y))
    
    def get_closest_enemy(self):
        """Restituisce il nemico più vicino al giocatore."""
        if not self.enemies:
            return None
        return min(self.enemies, key=lambda e: calculate_distance((self.player.x, self.player.y), (e.x, e.y)))

    def update_bullets(self, moving):
        """Gestisce lo sparo e il movimento dei proiettili."""
        self.bullet_timer += self.clock.get_time()
        if self.bullet_timer > self.bullet_interval and not moving:
            closest_enemy = self.get_closest_enemy()
            if closest_enemy:
                dx = closest_enemy.x - self.player.x
                dy = closest_enemy.y - self.player.y
                distance = calculate_distance((self.player.x, self.player.y), (closest_enemy.x, closest_enemy.y))
                if distance > 0:
                    dx /= distance
                    dy /= distance
                    self.bullets.append(Bullet(self.player.x, self.player.y, dx, dy))
            self.bullet_timer = 0

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_offscreen():
                self.bullets.remove(bullet)

    def update_enemies(self):
        """Muove i nemici e gestisce le collisioni con il giocatore."""
        for enemy in self.enemies[:]:
            enemy.move_towards(self.player.x, self.player.y)
            if self.player.is_colliding(enemy):
                self.player.take_damage(1)
                self.enemies.remove(enemy)

    
    def check_bullet_collisions(self):
        """Controlla le collisioni tra proiettili e nemici."""
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.check_collision(enemy):
                    if enemy.take_damage(self.player.attack): #se il nemico muore
                        if isinstance(enemy, BlackEnemy):
                            self.enemies.extend(enemy.spawn_red_enemies())
                            self.score += 9
                            self.experience += 1
                        elif isinstance(enemy, BlueEnemy):
                            self.score += 3
                            self.experience += 1
                        else:  # RedEnemy
                            self.score += 1
                            self.experience += 1
                        self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break  # Esci dal ciclo interno dopo la collisione

    def check_level_up(self):
        """Verifica se il giocatore deve salire di livello."""
        if self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level + self.level)
            self.level_up()

    def level_up(self):
        """Gestisce la logica del level up (mostra il menu)."""

        buffs = [
            {"name": "Heal", "action": lambda: self.player.heal(5)},
            {"name": "Max HP", "action": lambda: self.player.increase_max_health(2)},
            {"name": "Faster Reload", "action": lambda: self.reduce_bullet_interval(50)},
        ]

        selected_option = 0
        options_rects = draw_level_up_menu(self.screen, buffs, selected_option)  # Mostra menu

        waiting_for_selection = True
        while waiting_for_selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_option = (selected_option - 1) % len(buffs)
                    elif event.key == pygame.K_RIGHT:
                        selected_option = (selected_option + 1) % len(buffs)
                    elif event.key == pygame.K_RETURN:
                        buffs[selected_option]["action"]()
                        self.post_level_up()
                        waiting_for_selection = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(options_rects):
                        if rect.collidepoint(event.pos):
                            buffs[i]["action"]()
                            self.post_level_up()
                            waiting_for_selection = False
            
            # Aggiorna e ridisegna *solo* il menu, non l'intero gioco
            draw_level_up_menu(self.screen, buffs, selected_option)


    def post_level_up(self):
        """Azioni da eseguire dopo la selezione del buff."""
        self.score += self.player.health
        self.spawn_delay_timer = 0
        self.spawn_interval = INITIAL_SPAWN_INTERVAL

    def reduce_bullet_interval(self, amount):
        """Riduce il bullet interval (con un limite minimo)."""
        self.bullet_interval = max(200, self.bullet_interval - amount)
    
    def reset_game(self):
        """Resetta completamente lo stato del gioco per ricominciare."""
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.experience = 0
        self.level = 1
        self.exp_to_next_level = 10
        self.spawn_timer = 0
        self.spawn_interval = INITIAL_SPAWN_INTERVAL
        self.time_still = 0
        self.bullet_timer = 0
        self.bullet_interval = INITIAL_BULLET_INTERVAL
        self.spawn_delay_timer = 0
        # Non c'è bisogno di running = True, è già True all'inizio
        self.show_ui = False
EOF

cat << EOF > main.py
# main.py
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("arch-circle")

game = Game(screen)
game.run()
EOF

echo "Struttura del progetto creata con successo!"