import pygame
import random
from . import settings

vec = pygame.math.Vector2


class Enemy(settings.Setting):
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()

        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)

        self.radius = int(self.app.cell_width//2.3)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()

        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed

            # check whether its time to move
            if self.time_to_move():
                self.move()

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (
            self.pix_pos[0]-self.TOP_BOTTOM_BUFFER + self.app.cell_width//2
        )//self.app.cell_width+1

        self.grid_pos[1] = (
            self.pix_pos[1]-self.TOP_BOTTOM_BUFFER + self.app.cell_height//2
        )//self.app.cell_height+1

    def draw(self):
        # self.WIN.blit(self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)))
        pygame.draw.circle(
            self.app.screen,
            self.colour,
            (int(self.pix_pos.x),
             int(self.pix_pos.y)
             ),
            self.radius
        )

    def set_speed(self):
        '''Sets the speed of the enemy cells

        Returns:
            Integer: 2 if the personality is speedy or scared, otherwise 1
        '''
        return 2 if self.personality in ['speedy', 'scared'] else 1

    def set_target(self):
        if self.personality == 'speedy' or self.personality == 'slow':
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > self.COLS//2 and self.app.player.grid_pos[1] > self.ROWS//2:
                return vec(1, 1)

            if self.app.player.grid_pos[0] > self.COLS//2 and self.app.player.grid_pos[1] < self.ROWS//2:
                return vec(1, self.ROWS-2)

            if self.app.player.grid_pos[0] < self.COLS//2 and self.app.player.grid_pos[1] > self.ROWS//2:
                return vec(self.COLS-2, 1)

            else:
                return vec(self.COLS-2, self.ROWS-2)

    def time_to_move(self):
        '''Allows the enemy player to check whether it can move
        Returns:
            Boolean: True if the enemy cell can move in that direction
        '''
        if (int(self.pix_pos.x+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_width) == 0 and \
            self.direction == vec(1, 0) \
                or self.direction == vec(-1, 0) \
                or self.direction == vec(0, 0):
            return True
        if (int(self.pix_pos.y+self.TOP_BOTTOM_BUFFER//2) % self.app.cell_height) == 0 and \
            self.direction == vec(0, 1) \
                or self.direction == vec(0, -1) \
                or self.direction == vec(0, 0):
            return True
        return False

    def move(self):
        '''Allows the enemies to move'''
        self.direction = self.get_random_direction() \
            if self.personality == 'random' \
            else self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS(
            [int(self.grid_pos.x), int(self.grid_pos.y)],
            [int(target[0]), int(target[1])]
        )
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for _ in range(28)] for _ in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbor in neighbors:
                    if (neighbor[0]+current[0] >= 0
                        and neighbor[0] + current[0] < len(grid[0]) 
                        and neighbor[1]+current[1] >= 0 
                        and neighbor[1] + current[1] < len(grid)
                    ):
                        next_cell = [
                            neighbor[0] + current[0],
                            neighbor[1] + current[1]
                        ]

                        if next_cell not in visited and grid[next_cell[1]][next_cell[0]] != 1:
                            queue.append(next_cell)
                            path.append(
                                {'Current': current, 'Next': next_cell}
                            )
        shortest = [target]
        while target != start:
            for step in path:
                if step['Next'] == target:
                    target = step['Current']
                    shortest.insert(0, step['Current'])
        return shortest

    def get_random_direction(self):
        '''Gets a random direction for the enemy cells to move
        :return: The `X` and the `Y` direction
        '''
        while True:
            number = random.randint(-2, 1)

            if number == -2:
                x_dir, y_dir = 1, 0

            elif number == -1:
                x_dir, y_dir = 0, 1

            elif number == 0:
                x_dir, y_dir = -1, 0

            else:
                x_dir, y_dir = 0, -1

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:  # check whether the enemy cell is hitting a wall
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec(
            (self.grid_pos.x*self.app.cell_width) +
            self.TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2,

            (self.grid_pos.y*self.app.cell_height) +
            self.TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2
        )

    def set_colour(self):
        '''Sets the color of the enemy character'''
        possible_colors = {
            0: self.ENEMIES_BLUE,
            1: self.ENEMIES_YELLOW,
            2: self.ENEMIES_RED,
            3: self.ENEMIES_PINK
        }
        return possible_colors.get(self.number, self.ENEMIES_BLUE)

    def set_personality(self):
        personalities = {
            0: 'speedy',
            1: 'slow',
            2: 'random'
        }
        return personalities.get(self.number, 'scared')
