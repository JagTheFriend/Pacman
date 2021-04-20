import pygame


class Setting:
    '''
    These are important variables which is
    required to run the game
    '''

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
    PLAYER_COLOUR = (0, 255, 114)

    # back ground images
    IMAGES = [
        pygame.image.load('Assets/Pacman/maze original.png'),
        pygame.image.load('Assets/Pacman/maze purple.png'),
        pygame.image.load('Assets/Pacman/maze red.png'),
        pygame.image.load('Assets/Pacman/maze green.png'),
        pygame.image.load('Assets/Pacman/maze original.png')
    ]

    # font settings
    START_TEXT_SIZE = 16
    START_FONT = 'arial black'

    # load all the images
    # ENEMIES_BLUE = pygame.image.load(
    #     'Assets/Pacman/Virus - Blue.png'
    # )
    # ENEMIES_YELLOW = pygame.image.load(
    #     'Assets/Pacman/Virus - Green.png'
    # )
    # ENEMIES_RED = pygame.image.load(
    #     'Assets/Pacman/Virus - Purple.png'
    # )
    # ENEMIES_PINK = pygame.image.load(
    #     'Assets/Pacman/Virus - Pink.png'
    # )

    ENEMIES_BLUE = (43, 78, 203)
    ENEMIES_YELLOW = (197, 200, 27)
    ENEMIES_RED = (208, 22, 22)
    ENEMIES_PINK = (215, 159, 33)

    MUSIC = "Assets/Pacman/Pew.wav"

    # load important data
    GAME_WALLS = 'Assets/Pacman/walls.txt'
    SCORE = 'Assets/Pacman/score.txt'
    MAX_SCORE = [50, 100, 150, 200, 287]
