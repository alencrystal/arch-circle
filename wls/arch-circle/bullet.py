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
