import os
import pygame

class Animation:
    def __init__(self, player):
        self.player = player
        self.movement_sprites = self.load_movement_sprites()
        self.static_sprite = pygame.image.load("assets/images/character.png")
        self.current_sprite_index = 0
        self.animation_speed = 0.1
        self.time_accumulator = 0

    def load_movement_sprites(self):
        sprites = []
        path = "assets/images/movement_player"
        for file_name in sorted(os.listdir(path)):
            if file_name.endswith(".png"):
                sprites.append(pygame.image.load(os.path.join(path, file_name)))
        return sprites

    def update(self, delta_time):
        if self.player.is_moving():
            self.time_accumulator += delta_time
            if self.time_accumulator >= self.animation_speed:
                self.time_accumulator -= self.animation_speed  # Usa -= per mantenere il tempo residuo
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.movement_sprites)
            self.player.sprite = self.movement_sprites[self.current_sprite_index]
        else:
            self.player.sprite = self.static_sprite
            self.current_sprite_index = 0  # Resetta l'indice quando il player si ferma
