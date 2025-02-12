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
        self.speed_bonus = 1.0  # Aggiungi un bonus di velocità

    def move(self, keys):
        """Gestisce il movimento del giocatore in base ai tasti premuti."""
        if keys[pygame.K_UP] and self.y - self.radius > 0:
            self.y -= self.speed * self.speed_bonus
        if keys[pygame.K_DOWN] and self.y + self.radius < WINDOW_HEIGHT:
            self.y += self.speed * self.speed_bonus
        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed * self.speed_bonus
        if keys[pygame.K_RIGHT] and self.x + self.radius < WINDOW_WIDTH:
            self.x += self.speed * self.speed_bonus

    def draw(self, screen, offset_x, offset_y):
        """Disegna il giocatore e la barra della vita."""
        screen_x = self.x  # Rimuovi l'offset
        screen_y = self.y  # Rimuovi l'offset
        pygame.draw.circle(screen, BLACK, (screen_x, screen_y), self.radius + 2)
        pygame.draw.circle(screen, GREEN, (screen_x, screen_y), self.radius)

        # Barra della vita
        health_ratio = self.health / self.max_health
        current_health_bar_width = int(self.health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (screen_x - self.health_bar_width // 2, screen_y + self.radius + 10, self.health_bar_width, self.health_bar_height))
        pygame.draw.rect(screen, LIGHT_GREEN, (screen_x - self.health_bar_width // 2, screen_y + self.radius + 10, current_health_bar_width, self.health_bar_height))


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

    def increase_speed(self, percentage):
        """Incrementa la velocità di movimento del giocatore di una percentuale specifica."""
        self.speed_bonus += percentage
