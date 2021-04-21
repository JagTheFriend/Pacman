import pygame
import sys
import copy
from settings import *
from player_class import *
from enemy_class import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        try:
            with open(SCORE_FILE, 'r') as file:
                self.highest_score = int(file.read())

        except ValueError:
            self.highest_score = 0

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS

        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.lvl_counter = 0

        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()

            elif self.state == 'pause':
                self.start_events()
                self.pause_draw()

            elif self.state == 'level up':
                self.level_up_events()
                self.level_up_draw()

            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def pause_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(
            'PRESS ENTER TO PLAY',
            self.screen,
            [WIDTH//2, HEIGHT//2-50],
            START_TEXT_SIZE,
            (170, 132, 58),
            START_FONT,
            centered=True
        )
        self.draw_text(
            f'HIGHEST SCORE: {self.highest_score}',
            self.screen,
            [4, 0],
            START_TEXT_SIZE,
            (255, 255, 255),
            START_FONT
        )
        pygame.display.update()

    def level_up_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(
            f'GG, you leveled up to {self.lvl_counter}!, Press ENTER to continue..',
            self.screen,
            [WIDTH//2, HEIGHT//2-50],
            START_TEXT_SIZE,
            (170, 132, 58),
            START_FONT,
            centered=True
        )
        self.draw_text(
            f'HIGHEST SCORE: {self.highest_score}',
            self.screen,
            [4, 0],
            START_TEXT_SIZE,
            (255, 255, 255),
            START_FONT
        )
        pygame.display.update()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load(MAPS[self.lvl_counter])
        self.background = pygame.transform.scale(
            self.background, (MAZE_WIDTH, MAZE_HEIGHT)
        )

        # Opening walls file
        # Creating walls list with co-ordinates of walls
        # stored as  a vector
        with open(GAME_WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))

                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))

                    elif char == 'P':
                        self.p_pos = [xidx, yidx]

                    elif char in ['2', '3', '4', '5']:
                        self.e_pos.append([xidx, yidx])

                    elif char == 'B':
                        pygame.draw.rect(
                            self.background,
                            BLACK,
                            (xidx*self.cell_width,
                             yidx*self.cell_height,
                             self.cell_width,
                             self.cell_height
                             )
                        )

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))

        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

    def reset(self):
        
        if self.player.current_score > self.highest_score:
            self.highest_score = self.player.current_score

            with open(SCORE_FILE, "w") as file:
                file.write(str(self.player.current_score))
                
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
        with open(GAME_WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = 'playing'

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self.state = 'playing'

    def level_up_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self.player.current_score = 0
                self.player.grid_pos = vec(self.player.starting_pos)
                self.player.pix_pos = self.player.get_pix_pos()
                self.player.direction *= 0

                for enemy in self.enemies:
                    enemy.grid_pos = vec(enemy.starting_pos)
                    enemy.pix_pos = enemy.get_pix_pos()
                    enemy.direction *= 0

                self.coins = []
                with open(GAME_WALLS, 'r') as file:
                    for yidx, line in enumerate(file):
                        for xidx, char in enumerate(line):
                            if char == 'C':
                                self.coins.append(vec(xidx, yidx))

                self.state = 'playing'
                self.state = 'playing'

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(
            'PRESS ENTER TO PLAY',
            self.screen,
            [WIDTH//2, HEIGHT//2-50],
            START_TEXT_SIZE,
            (170, 132, 58),
            START_FONT,
            centered=True
        )

        self.draw_text(
            '1 PLAYER ONLY',
            self.screen,
            [WIDTH//2, HEIGHT//2+50],
            START_TEXT_SIZE,
            (44, 167, 198),
            START_FONT,
            centered=True
        )
        self.draw_text(
            f'HIGHEST SCORE: {self.highest_score}',
            self.screen,
            [4, 0],
            START_TEXT_SIZE,
            (255, 255, 255),
            START_FONT
        )
        pygame.display.update()

    def playing_events(self):
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

                if event.key in [pygame.K_p]:
                    self.state = 'pause'

                if event.key in [pygame.K_DOWN, pygame.K_f]:
                    sys.exit()

            if NEXT_LEVEL[self.lvl_counter] < self.player.current_score:
                self.lvl_counter += 1
                self.state = 'level up'

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(
            self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2)
        )
        # if self.player.current_score > self.highest_score:
        #     self.highest_score = self.player.current_score

        #     with open(SCORE_FILE, "w") as file:
        #         file.write(str(self.player.current_score))

        self.draw_coins()
        # self.draw_grid()
        self.draw_text(f'CURRENT SCORE: {self.player.current_score}',
                       self.screen, [60, 0], 18, WHITE, START_FONT)

        self.draw_text(f'HIGH SCORE: {self.highest_score}', self.screen, [
                       WIDTH//2+60, 0], 18, WHITE, START_FONT)

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'game over'
        else:
            if self.player.current_score > self.highest_score:
                self.highest_score = self.player.current_score

                with open(SCORE_FILE, "w") as file:
                    file.write(str(self.player.current_score))

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
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self.reset()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = 'Press the escape button to QUIT'
        again_text = 'Press ENTER to PLAY AGAIN'
        self.draw_text(
            'GAME OVER',
            self.screen,
            [WIDTH//2, 100],
            52,
            RED,
            'arial',
            centered=True
        )
        self.draw_text(
            again_text,
            self.screen,
            [WIDTH//2, HEIGHT//2],
            36,
            (190, 190, 190),
            'arial',
            centered=True
        )
        self.draw_text(
            quit_text,
            self.screen,
            [WIDTH//2, HEIGHT//1.5],
            36,
            (190, 190, 190),
            'arial',
            centered=True
        )
        pygame.display.update()
