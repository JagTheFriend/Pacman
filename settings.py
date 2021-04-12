import pygame
import os


class Setting:
    """
    These are important variables which is
    required to run the game
    """

    # screen settings
    WIDTH = 610
    HEIGHT = 670
    FPS = 60
    TOP_BOTTOM_BUFFER = 50

    MAZE_WIDTH = WIDTH-TOP_BOTTOM_BUFFER
    MAZE_HEIGHT = HEIGHT-TOP_BOTTOM_BUFFER

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    ROWS = 30
    COLS = 28

    # colour settings
    BLACK = (0, 0, 0)
    RED = (208, 22, 22)
    GREY = (107, 107, 107)
    WHITE = (255, 255, 255)
    PLAYER_COLOUR = (190, 194, 15)

    # font settings
    START_TEXT_SIZE = 16
    START_FONT = "arial black"

    ENEMIES_BLUE = pygame.image.load(
        os.path.join("Assets", "Virus - Blue.png")
    )
    ENEMIES_YELLOW = pygame.image.load(
        os.path.join("Assets", "Virus - Green.png")
    )
    ENEMIES_RED = pygame.image.load(
        os.path.join("Assets", "Virus - Purple.png")
    )
    ENEMIES_PINK = pygame.image.load(
        os.path.join("Assets", "Virus - Pink.png")
    )
