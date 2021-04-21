import pygame

# screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

MAIN_PLAYER_COLOUR = pygame.image.load("Assets/Game Player16.png")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

MAPS = [
    'Assets\maze original.png',
    'Assets\maze purple.png',
    'Assets\maze red.png',
    'Assets\maze green.png',
    'Assets\maze original.png'
]

GAME_WALLS = 'Assets\walls.txt'
SCORE_FILE = 'Assets\score.txt'

NEXT_LEVEL = [
    50, 100, 150, 200, 287
]
