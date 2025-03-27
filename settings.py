# settings.py
import pygame

pygame.init()

# Configurazioni finestra
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
BACKGROUND_IMAGE = "images/floor_wood.jpg"

# Configurazioni colori
GREEN = (35, 101, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
YELLOW = (222, 208, 108)

# Configurazioni giocatore
DEFAULT_RADIUS = 20
PLAYER_SPEED = 5
MAX_HEALTH = 10
HEALTH_BAR_WIDTH = 50
HEALTH_BAR_HEIGHT = 5
PLAYER_ATTACK = 1

# Configurazioni proiettili
BULLET_RADIUS = 5
BULLET_SPEED = 7
BULLET_INTERVAL = 1000

# Configurazioni nemici
ENEMY_RADIUS = 10
BLACK_ENEMY_RADIUS = 15
RED_ENEMY_SPEED = 1.5
BLUE_ENEMY_HP = 2
BLUE_ENEMY_SPEED = 1
BLACK_ENEMY_HP = 5
BLACK_ENEMY_SPEED = 0.8

# Configurazioni spawn
SPAWN_INTERVAL = 1000
MIN_SPAWN_INTERVAL = 200
SPAWN_DELAY = 3

# Font
FONT_PATH = "font/Titillium.ttf"
font_small = pygame.font.Font(FONT_PATH, 30)
font_large = pygame.font.Font(FONT_PATH, 74)

