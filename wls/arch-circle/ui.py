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
