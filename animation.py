import os
import pygame

class Animation:
    def __init__(self, player):
        # Inizializza l'animazione associata a un oggetto player
        self.player = player
        # Carica i frame di animazione per il movimento del giocatore
        self.movement_sprites = self.load_sprites("assets/images/movement_player")
        # Carica lo sprite statico del giocatore (quando non si muove)
        self.static_sprite = self.load_sprite("assets/images/character.png")
        # Indice del frame corrente nell'animazione
        self.current_sprite_index = 0
        # Velocità dell'animazione (tempo tra i frame)
        self.animation_speed = 0.2  # Tempo in secondi
        # Accumulatore di tempo per gestire il cambio di frame
        self.time_accumulator = 0

    def load_sprites(self, path):
        # Carica tutti i file immagine (.png) dalla directory specificata
        sprites = []
        for file_name in sorted(os.listdir(path)):
            if file_name.endswith(".png"):
                # Debug: stampa i file caricati
                print(f"Caricamento sprite da {path}: {file_name}")
                sprites.append(self.load_sprite(os.path.join(path, file_name)))
        return sprites

    def load_sprite(self, path):
        # Carica un singolo file immagine come sprite
        return pygame.image.load(path)

    def update(self, delta_time):
        # Aggiorna l'animazione in base al tempo trascorso e allo stato del giocatore
        if self.player.is_moving():
            # Incrementa il tempo accumulato
            self.time_accumulator += delta_time
            # Cambia frame se è trascorso abbastanza tempo
            if self.time_accumulator >= self.animation_speed:
                self.time_accumulator = 0
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.movement_sprites)
            # Imposta lo sprite corrente del giocatore al frame attuale
            self.player.sprite = self.movement_sprites[self.current_sprite_index]
        else:
            # Se il giocatore non si muove, usa lo sprite statico
            self.player.sprite = self.static_sprite

        # Ridimensiona lo sprite del giocatore per adattarlo alla dimensione originale
        self.player.sprite = pygame.transform.scale(self.player.sprite, (self.player.radius * 2, self.player.radius * 2))

        # Specchia lo sprite se il giocatore si muove a sinistra
        if self.player.flipped:
            self.player.sprite = pygame.transform.flip(self.player.sprite, True, False)

        # Debug: verifica che il frame corrente corrisponda all'immagine corretta
        print(f"Frame corrente: {self.current_sprite_index}, Sprite: {self.movement_sprites[self.current_sprite_index]}")
