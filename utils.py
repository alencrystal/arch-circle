# utils.py
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT

def random_spawn_position():
    """Genera una posizione casuale ai bordi dello schermo."""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return random.randint(0, WINDOW_WIDTH), 0
    elif side == "bottom":
        return random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT
    elif side == "left":
        return 0, random.randint(0, WINDOW_HEIGHT)
    elif side == "right":
        return WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT)


def calculate_distance(pos1, pos2):
    """Calcola la distanza tra due punti (x, y)."""
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
