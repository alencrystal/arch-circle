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
