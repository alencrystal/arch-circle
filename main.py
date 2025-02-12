# main.py
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("arch-circle")

game = Game(screen)
game.run()
