import pygame
import sys
from . import settings
from . import player_class
from . import enemy_class


pygame.init()
vec = pygame.math.Vector2

first_time = True


class App(settings.Setting):
    def __init__(self):
        self.screen = self.WIN
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'

        self.cell_width = self.MAZE_WIDTH//self.COLS
        self.cell_height = self.MAZE_HEIGHT//self.ROWS
        self.walls = []
        self.coins = []

        self.enemies = []
        self.enemies_pos = []
        self.p_pos = None

        self.lvl_counter = 0
        self.map_counter = 1

        self.load()
        self.player = player_class.Player(self, vec(self.p_pos))
        self.make_enemies()  # making enemies

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

                # fixing a bug where the player has less than 3 lives
                # when the game is first started
                if globals().get('first_time', True):
                    globals()['first_time'] = False
                    self.player.lives = 3

            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()

            elif self.state == 'level':
                self.start_events()
                self.level_up_draw()

            elif self.state == 'wait':
                self.start_events()

            else:
                self.running = False
            self.clock.tick(self.FPS)
        pygame.quit()
        print('\nThanks for playing the game x)\n')
        sys.exit()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()

        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self, image='Back Ground'):
        '''Creates the map'''
        self.background = (
            self.IMAGES[0]
            if image == 'Back Ground'
            else self.IMAGES[self.map_counter]
        )
        self.background = pygame.transform.scale(
            self.background, (self.MAZE_WIDTH, self.MAZE_HEIGHT)
        )

        # Opening walls file
        # Creating walls list with co-ordinates of walls
        # stored as a vector
        with open(self.GAME_WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))

                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))

                    elif char == 'P':
                        self.p_pos = [xidx, yidx]

                    elif char in ['2', '3', '4', '5']:
                        self.enemies_pos.append([xidx, yidx])

                    elif char == 'B':
                        pygame.draw.rect(
                            self.background, self.BLACK, (
                                xidx*self.cell_width, yidx*self.cell_height,
                                self.cell_width, self.cell_height
                            )
                        )

    def level_up_draw(self):
        '''This is the level up screen'''
        if self.old_score < self.player.current_score:
            self.old_score = self.player.current_score

        self.screen.fill(self.BLACK)
        self.draw_text(
            f'GG, you leveled up to: {1 if self.lvl_counter == 0 else self.lvl_counter}',
            self.screen,
            [self.WIDTH//2, self.HEIGHT//2-50],
            self.START_TEXT_SIZE,
            (170, 132, 58),
            self.START_FONT,
            centered=True
        )

        self.draw_text(
            f'HIGHEST SCORE: {self.old_score}',
            self.screen,
            [4, 0],
            self.START_TEXT_SIZE,
            (255, 255, 255),
            self.START_FONT
        )
        self.lvl_counter += 1
        self.player.current_score = 0
        self.state = 'wait'

        self.load(self.IMAGES[self.lvl_counter])
        pygame.display.update()

    def make_enemies(self):
        for idx, pos in enumerate(self.enemies_pos):
            self.enemies.append(enemy_class.Enemy(self, vec(pos), idx))

    def draw_grid(self):
        '''
        Draws the board
        '''
        for x in range(self.WIDTH//self.cell_width):
            pygame.draw.line(
                self.background,
                self.GREY,
                (x*self.cell_width, 0),
                (x*self.cell_width, self.HEIGHT)
            )

        for x in range(self.HEIGHT//self.cell_height):
            pygame.draw.line(
                self.background,
                self.GREY,
                (0, x*self.cell_height),
                (self.WIDTH, x*self.cell_height)
            )

        for coin in self.coins:
            pygame.draw.rect(
                self.background,
                (167, 179, 34), (
                    coin.x*self.cell_width,
                    coin.y*self.cell_height,
                    self.cell_width,
                    self.cell_height
                )
            )

    def reset(self):
        '''
        Resets the board
        '''

        # keep track of the highest score
        if self.old_score < self.player.current_score:
            self.old_score = self.player.current_score

        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)

        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open(self.GAME_WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = 'playing'

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'playing'

    def start_draw(self):
        '''
        This is the startup screen
        '''
        self.screen.fill(self.BLACK)
        self.draw_text(
            'Press ENTER to play',
            self.screen,
            [self.WIDTH//2, self.HEIGHT//2-50],
            self.START_TEXT_SIZE,
            (170, 132, 58),
            self.START_FONT,
            centered=True
        )

        self.draw_text(
            '1 PLAYER ONLY',
            self.screen,
            [self.WIDTH//2, self.HEIGHT//2+50],
            self.START_TEXT_SIZE,
            (44, 167, 198),
            self.START_FONT, centered=True
        )

        with open(self.SCORE, 'r') as file:
            self.old_score = int(file.read())

        self.draw_text(
            f'HIGHEST SCORE: {self.old_score}',
            self.screen,
            [4, 0],
            self.START_TEXT_SIZE,
            (255, 255, 255),
            self.START_FONT
        )

        pygame.display.update()

    def playing_events(self):
        '''
        Gets all the instructions 
        such as pressing keys etc,
        and process it

        A - left arrow key(⬅️) Going to the right
        S - down arrow key(⬇️) - Going down
        W - up arrow key(⬆️) - Going up
        D - right arrow key(➡️) - Going to the left
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.player.move(vec(-1, 0))

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.player.move(vec(1, 0))

                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.player.move(vec(0, -1))

                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.player.move(vec(0, 1))

                elif self.player.current_score > self.MAX_SCORE[self.lvl_counter]:
                    self.player.current_score = 0
                    self.state = 'level'
                    return 

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            # the player got killed
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(
            self.background, (self.TOP_BOTTOM_BUFFER//2, self.TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text(
            f'CURRENT SCORE: {self.player.current_score}',
            self.screen,
            [60, 0],
            18,
            self.WHITE,
            self.START_FONT
        )

        self.draw_text(
            f'HIGH SCORE: {self.old_score}',
            self.screen,
            [self.WIDTH//2+60, 0],
            18,
            self.WHITE,
            self.START_FONT
        )

        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()  # drawing the enemies

        # updating the display
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'game over'
        else:
            # keep track of the highest score
            if self.old_score < self.player.current_score:
                self.old_score = self.player.current_score

            self.player.current_score = 0

            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0

            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(
                self.screen,
                (124, 123, 7),
                (
                    int(coin.x*self.cell_width) +
                    self.cell_width//2+self.TOP_BOTTOM_BUFFER//2,
                    int(coin.y*self.cell_height) +
                    self.cell_height//2+self.TOP_BOTTOM_BUFFER//2
                ),
                5
            )

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.old_score < self.player.current_score:
                    self.old_score = self.player.current_score
                # storing the new high score
                with open(self.SCORE, 'w') as file:
                    file.write(str(self.old_score))

                self.running = False

    def game_over_draw(self):
        self.screen.fill(self.BLACK)
        quit_text = 'To quit, press ESCAPE'
        again_text = 'To play again, press ENTER'
        self.draw_text(
            'GAME OVER',
            self.screen,
            [self.WIDTH//2, 100],
            52,
            self.RED,
            'arial',
            centered=True
        )

        self.draw_text(
            again_text, self.screen, [
                self.WIDTH//2, self.HEIGHT//2],  36, (190, 190, 190), 'arial', centered=True)

        self.draw_text(
            quit_text,
            self.screen,
            [self.WIDTH//2, self.HEIGHT//1.5],
            36,
            (190, 190, 190),
            'arial',
            centered=True
        )
        pygame.display.update()
