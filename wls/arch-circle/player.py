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
