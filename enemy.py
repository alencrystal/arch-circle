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

    def draw(self, screen, offset_x, offset_y):
        """Disegna il nemico."""
        screen_x = self.x  # Rimuovi l'offset
        screen_y = self.y  # Rimuovi l'offset
        pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.radius + 2)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)

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
