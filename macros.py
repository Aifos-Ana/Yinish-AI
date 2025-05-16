import pygame
import math


# Constants
WIDTH, HEIGHT = 800, 800
BG_COLOR = (255, 255, 255)
HEX_RADIUS = 40
CIRCLE_RADIUS = 30  # Size of stones
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BOARD_SIZE = 5  # Hexagon size

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BRIGHT_BLUE = (173, 216, 230)  
BRIGHT_RED = (255, 182, 193)   

RINGS_AVAIL_WHITE=5
RINGS_AVAIL_BLACK=5

MARKER_AVAIL= 5

IDLE_RING_COLOR = (128, 128, 128)  
GUI_RING_POSITIONS = [
    (WIDTH - 150, 50), (WIDTH - 90, 50), (WIDTH - 30, 50),  # Top-right
    (30, HEIGHT - 50), (90, HEIGHT - 50), (150, HEIGHT - 50)  # Bottom-left
]

RING_MARGIN_LOOKUP = {
            (3, 0): 10, (3, 1): 9, (3, 2): 8,
            (2, 0): 7, (2, 1): 6, (2, 2): 5,
            (1, 0): 6, (1, 1): 5, (1, 2): 4,
            (0, 0): 5, (0, 1): 4, (0, 2): 3,
            (2, 3): 2, (1, 3): 1, (0, 3): 0
        }

PLAYER_1 = 1
PLAYER_2 = 2


MINIMAX_ALGHORITM = 3
MONTE_CARLO_ALGHORITM = 4


