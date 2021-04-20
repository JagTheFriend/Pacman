import pygame
from . import settings

vec = pygame.math.Vector2

pygame.mixer.init()
class Player(settings.Setting):
    def __init__(self, app, pos):
        self.COIN_SOUND = pygame.mixer.Sound(self.MUSIC)

        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos

        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None

        self.able_to_move = True
        self.current_score = 0
        self.speed = 2

        self.lives = 1

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - self.TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1

        self.grid_pos[1] = (self.pix_pos[1]-self.TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

        if self.on_coin():  # if the player is on a coin, then the coin disappears
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(
            self.app.screen,
            self.PLAYER_COLOUR,
            (int(self.pix_pos.x),
             int(self.pix_pos.y)
             ),
            self.app.cell_width//2-2
        )

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(
                self.app.screen,
                self.PLAYER_COLOUR,
                (30 + 20*x, self.HEIGHT - 15),
                7
            )

    def on_coin(self) -> bool:
        '''
        Checks whether the player is on a coin
        :return: Boolean
        '''
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0 and \
                    self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True

            if int(self.pix_pos.y+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 and \
                    self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1
        self.COIN_SOUND.play()

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+self.TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   self.TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0 and \
                self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
            return True

        if int(self.pix_pos.y+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 and \
                self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
            return True

    def can_move(self):
        '''
        Checks whether the player can move in that particular direction
        :return: Boolean
        '''
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
