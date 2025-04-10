# player.py
import pygame
from config import *
from animation import Animation

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
        self.image = pygame.image.load("assets/images/character.png")  # Load the character image
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # Scale to fit the player size
        self.flipped = False  # Track if the image is flipped
        self.animation = Animation(self)

    def move(self, keys):
        """Gestisce il movimento del giocatore in base ai tasti premuti."""
        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed * self.speed_bonus
            if not self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
                self.flipped = True
        if keys[pygame.K_RIGHT] and self.x + self.radius < WINDOW_WIDTH:
            self.x += self.speed * self.speed_bonus
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)  # Reset to original
                self.flipped = False
        if keys[pygame.K_UP] and self.y - self.radius > 0:
            self.y -= self.speed * self.speed_bonus
        if keys[pygame.K_DOWN] and self.y + self.radius < WINDOW_HEIGHT:
            self.y += self.speed * self.speed_bonus

    def draw(self, screen, offset_x, offset_y):
        """Disegna il giocatore e la barra della vita."""
        screen_x = self.x - self.radius  # Adjust for image centering
        screen_y = self.y - self.radius  # Adjust for image centering
        # Usa lo sprite aggiornato dall'animazione invece dell'immagine statica
        screen.blit(self.sprite, (screen_x, screen_y))  # Draw the current sprite

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

    def increase_speed(self, percentage):
        """Incrementa la velocità di movimento del giocatore di una percentuale specifica."""
        self.speed_bonus += percentage

    def is_moving(self):
        """Controlla se il player si sta muovendo."""
        # Controlla se il giocatore si sta muovendo in base alla velocità o ai tasti premuti
        keys = pygame.key.get_pressed()
        return keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]

    def update(self, delta_time):
        """Aggiorna lo stato del giocatore."""
        self.animation.update(delta_time)
