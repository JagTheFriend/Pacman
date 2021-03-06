import pygame

WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

MAIN_PLAYER_COLOUR = pygame.image.load("Assets/Game Player16.png")

BUE_ENEMY = pygame.image.load("Assets/Virus - Blue16.png")
RED_ENEMY = pygame.image.load("Assets/Virus - Pink16.png")
GREEN_ENEMY = pygame.image.load("Assets/Virus - Green16.png")
PURPLE_ENEMY = pygame.image.load("Assets/Virus - Purple16.png")

COIN_COLOR = pygame.image.load("Assets/mask.png")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

START_TEXT_SIZE = 16
START_FONT = 'arial black'

MAPS = [
    'Assets/maze original.png',
    'Assets/maze purple.png',
    'Assets/maze red.png',
    'Assets/maze green.png',
    'Assets/maze original.png'
]

GAME_WALLS = 'Assets/walls.txt'
SCORE_FILE = 'Assets/score.txt'

NEXT_LEVEL = [
    50, 100, 150, 200, 287
]
REDUCE_VELOCITY = 0.375
