# game.py
import pygame
import sys
import random
import os  # Add import for os
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
        self.spawn_interval = INITIAL_SPAWN_INTERVAL  # Use the fixed spawn interval
        self.min_spawn_interval = MIN_SPAWN_INTERVAL  # Ensure the minimum spawn interval is also fixed
        self.spawn_delay_timer = 0
        self.time_still = 0
        self.bullet_timer = 0
        self.bullet_interval = INITIAL_BULLET_INTERVAL
        self.running = True
        self.show_ui = False
        self.background_names = []  # Store the names of the background images
        self.background_images, self.background_names = self.load_background_images("assets/images/floor")
        self.background = random.choice(self.background_images)  # Randomly select the initial background
        self.background_name = self.background_names[self.background_images.index(self.background)]
        self.game_over = False  # Add game over flag
        self.enemies_to_spawn = self.exp_to_next_level  # Track the number of enemies to spawn

    def load_background_images(self, folder_path):
        """Carica tutte le immagini di sfondo dalla cartella specificata."""
        images = []
        names = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder_path, filename))
                image = pygame.transform.scale(image, (256, 256))
                images.append(image)
                names.append(filename)
        return images, names

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
                if event.key == pygame.K_RETURN and self.enemies_to_spawn == 0 and not self.enemies and self.check_door_collision():
                    self.level_up()

    def update(self):
        """Aggiorna la logica di gioco (movimento, collisioni, ecc.)."""
        keys = pygame.key.get_pressed()
        moving = any([keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]])
        self.player.move(keys)

        # Spawn nemici
        if self.enemies_to_spawn > 0:
            self.update_spawn_logic(moving)

        # Sparo proiettili
        self.update_bullets(moving)

        # Movimento nemici e collisioni
        self.update_enemies()

        # Controllo collisioni proiettili
        self.check_bullet_collisions()
        
        # Check if all required enemies are defeated and player reaches the door
        if self.enemies_to_spawn == 0 and not self.enemies:
            if self.check_door_collision():
                self.level_up()

        # Game over
        if self.player.health <= 0:
            self.game_over = True  # Set game over flag
            draw_game_over_screen(self.screen, self.score, self.level)
            pygame.display.flip()  # Ensure the screen is updated

        # Aggiorna l'animazione del giocatore
        self.player.update(self.clock.get_time() / 1000.0)

        # Debug: verifica lo stato del giocatore e dell'animazione
        print(f"Player position: ({self.player.x}, {self.player.y})")
        print(f"Player is moving: {self.player.is_moving()}")
        print(f"Current animation frame: {self.player.animation.current_sprite_index}")

    def draw(self):
        """Disegna tutti gli elementi del gioco."""
        # Rimuovi il calcolo dell'offset
        # offset_x = min(max(self.player.x - WINDOW_WIDTH // 2, 0), MAP_WIDTH - WINDOW_WIDTH)
        # offset_y = min(max(self.player.y - WINDOW_HEIGHT // 2, 0), MAP_HEIGHT - WINDOW_HEIGHT)

        # Disegna lo sfondo
        draw_tiled_background(self.screen, self.background, self.background_name)

        # Disegna il giocatore
        self.player.draw(self.screen, 0, 0)

        # Disegna i nemici
        for enemy in self.enemies:
            enemy.draw(self.screen, 0, 0)

        # Disegna i proiettili
        for bullet in self.bullets:
            bullet.draw(self.screen, 0, 0)

        # Disegna il punteggio
        draw_score(self.screen, self.score)

        # Disegna la UI se visibile
        if self.show_ui:
            draw_ui(self.screen, self.player, self.experience, self.bullet_interval)

        # Disegna la schermata di game over se il gioco è finito
        if self.game_over:
            self.screen.fill(BLACK)  # Clear the screen
            draw_game_over_screen(self.screen, self.score, self.level)

        # Disegna la porta se tutti i nemici richiesti sono stati sconfitti
        if self.enemies_to_spawn == 0 and not self.enemies:
            self.draw_door()

        pygame.display.flip()


    def run(self):
        """Ciclo principale del gioco."""
        while self.running:
            self.handle_input()
            if not self.game_over:  # Update and draw only if not game over
                self.update()
                self.draw()
            self.clock.tick(60)

    def update_spawn_logic(self, moving):
        """Logica per lo spawn dei nemici."""
        self.spawn_timer += self.clock.get_time()
        if self.spawn_timer > self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0
            self.enemies_to_spawn -= 1  # Decrement the number of enemies to spawn

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
            self.level += 1  # Increment the level
            self.exp_to_next_level = int(self.exp_to_next_level + self.level)
            self.level_up()

    def level_up(self):
        """Gestisce la logica del level up (mostra il menu)."""

        # Pool di potenziamenti disponibili
        all_buffs = [
            {"name": "Heal", "action": lambda: self.player.heal(5)},
            {"name": "Max HP", "action": lambda: self.player.increase_max_health(2)},
            {"name": "Faster Reload", "action": lambda: self.reduce_bullet_interval(50)},
            {"name": "Move Speed", "action": lambda: self.player.increase_speed(0.05)},  # Nuovo potenziamento
            {"name": "Extra Score", "action": lambda: self.increase_score(0.05)}  # Nuovo potenziamento
        ]

        # Seleziona casualmente 3 potenziamenti dal pool
        buffs = random.sample(all_buffs, 3)

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

        # Transport the player to a new room
        self.player.x = WINDOW_WIDTH // 2
        self.player.y = WINDOW_HEIGHT // 2
        self.enemies = []
        self.spawn_timer = 0
        self.bullet_timer = 0
        self.experience = 0
        self.exp_to_next_level += 10
        self.enemies_to_spawn = self.exp_to_next_level  # Reset the number of enemies to spawn
        self.background = random.choice(self.background_images)  # Change the background
        self.background_name = self.background_names[self.background_images.index(self.background)]

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
        self.game_over = False  # Reset game over flag

    def increase_score(self, percentage):
        """Aggiunge al punteggio attuale del giocatore un bonus del 5%."""
        self.score += int(self.score * percentage)

    def draw_door(self):
        """Disegna una porta in alto al centro dello schermo."""
        door_image = pygame.image.load("assets/images/stairs.png")
        door_image = pygame.transform.scale(door_image, (50, 50))
        door_x = (WINDOW_WIDTH - door_image.get_width()) // 2
        door_y = 0
        self.screen.blit(door_image, (door_x, door_y))

    def check_door_collision(self):
        """Controlla se il giocatore ha raggiunto la porta."""
        door_width = 40
        door_height = 40
        door_x = (WINDOW_WIDTH - door_width) // 2
        door_y = 0
        player_rect = pygame.Rect(self.player.x - self.player.radius, self.player.y - self.player.radius, self.player.radius * 2, self.player.radius * 2)
        door_rect = pygame.Rect(door_x, door_y, door_width, door_height)
        return player_rect.colliderect(door_rect)
