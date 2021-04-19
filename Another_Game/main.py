import pygame
import random

pygame.font.init()

# making the window
WIDTH = HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
# Load images
RED_SPACE_SHIP = pygame.image.load(
    "Assets/Another Game/Virus - Pink.png"
)
GREEN_SPACE_SHIP = pygame.image.load(
    "Assets/Another Game/Virus - Green.png"
)
BLUE_SPACE_SHIP = pygame.image.load(
    "Assets/Another Game/Virus - Purple.png"
)

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(
    "Assets/Another Game/pixel_ship_yellow_small.png"
)

# Lasers
RED_LASER = pygame.image.load(
    "Assets/Another Game/pixel_laser_red.png"
)
GREEN_LASER = pygame.image.load(
    "Assets/Another Game/pixel_laser_green.png"
)
BLUE_LASER = pygame.image.load(
    "Assets/Another Game/pixel_laser_blue.png"
)
YELLOW_LASER = pygame.image.load(
    "Assets/Another Game/pixel_laser_yellow.png"
)

# Background
BG = pygame.transform.scale(
    pygame.image.load(
        "Assets/Another Game/background.png"
    ),
    (WIDTH, HEIGHT)
)

# all the colours of the ship
COLORS: [str] = ["red", "blue", "green"]


# end line
END_LINE = "\nThanks for playing the game xD"


class Laser:
    """
    Makes the laser
    which shows up when the player and enemy ship(s)
    shoot at each other
    """

    def __init__(self, x: int, y: int, img: pygame.image):
        # position of the laser
        self.x = x
        self.y = y

        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window: pygame.display):
        """
        Updates the window
        """
        window.blit(self.img, (self.x, self.y))

    def move(self, vel: int):
        """
        Allows the laser to travel
        DOWN the main screen
        """
        self.y += vel

    def off_screen(self, height: int) -> bool:
        """
        To check whether the laser is outside the main screen
        :return: Boolean
        """
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj: object):
        """
        Checks whether the laser collided with an object(or a ship)
        :return: collide(self, obj)
        """
        return collide(self, obj)


class Ship:
    """
    This is the base class
    Which allows other class(es) to get the same functionality

    Which means that every ship would behave the same, and 
    it can do the same things
    """
    COOLDOWN_COUNTER = 30  # delay between shooting lasers

    def __init__(self, x: float, y: float, health: int = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window: pygame.display):
        """
        Draws the laser
        """
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel: int, obj: object):
        """
        Allows the laser to move though the screen
        (creates an animation of a moving laser)
        """
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # checking whether the laser is off the screen
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # cheking whether the laser hit something
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        """
        Limiting the number of laser which could be shot per second
        """
        if self.cool_down_counter >= self.COOLDOWN_COUNTER:
            self.cool_down_counter = 0

        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        """
        Allows the enemy and the player to be able to shoot lasers
        """
        if self.cool_down_counter == 0:  # check the time difference between 2 adjacent lasers
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self) -> float:
        """
        Gets the width of the ship image
        :return: Float
        """
        return self.ship_img.get_width()

    def get_height(self) -> float:
        """
        Gets the height of the ship image
        :return: Float
        """
        return self.ship_img.get_height()


class Player(Ship):
    """
    Makes a player
    Extends `Ship`
    """

    def __init__(self, x: float, y: float, health: int = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel: int, objs: list):
        """
        Checks whether the laser collided with an object(or a ship)
        and removes it from the screen
        """
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)

            # the laser didn't do anything
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
                continue

            # the laser hits the enemy ship
            for obj in objs:
                if laser.collision(obj):
                    objs.remove(obj)
                    if laser in self.lasers:
                        self.lasers.remove(laser)

    def draw(self, window: pygame.display):
        """
        To draw the laser, player's ship
        """
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window: pygame.display):
        """
        Shows the health bar of the player's ship
        """
        # default health value is 100
        pygame.draw.rect(
            # the box filed with red
            window, (255, 0, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(), 10
            )
        )

        pygame.draw.rect(
            # the box is filled with green color
            window, (0, 255, 0),
            (
                self.x, self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * (self.health/self.max_health),
                10
            )
        )


class Enemy(Ship):
    """
    Creates the enemies
    Extends `Ship`
    """
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x: float, y: float, color: str, health: int = 100):
        super().__init__(x, y, health)
        # gives the ship image and laser image
        # color is randomly picked
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel: int):
        """
        Allows the enemy ship to only move downwards
        """
        self.y += vel

    def shoot(self):
        """
        Allowing the enemy ships to shoot lasers
        """
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2: object) -> bool:
    """
    Checks whether the laser collided with an object(or a ship)
    :return: Boolean
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def redraw_window(
    *,
    main_font: pygame.font.SysFont,
    lives: int,
    level: int,
    enemies: list,
    player: Player,
    lost: bool,
    lost_font: pygame.font.SysFont
) -> None:
    """
    Updates things such as `Current Score` etc 
    and displays it on the window
    """
    WIN.blit(BG, (0, 0))

    # draw text
    lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

    # to show the enemies
    for enemy in enemies:
        enemy.draw(WIN)

    # to draw the player
    player.draw(WIN)

    if lost:  # check whether the player has lost
        lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
        WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

    pygame.display.update()


def check_keys(*, player: Player, player_vel: int):
    # to check whether an user quit or not
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(END_LINE)
                pygame.quit()
    except pygame.error:
        pygame.quit()

    try:
        # to get the key pressed
        keys = pygame.key.get_pressed()
    except pygame.error:  # alt+f4 etc was done
        exit(code=69)

    # a for going to the left until the border comes up
    if keys[pygame.K_a] and (player.x - player_vel) > 0:  # left
        player.x -= player_vel

    # d for going to the right until the border comes up
    if keys[pygame.K_d] and (player.x + player_vel + player.get_width()) < WIDTH:  # right
        player.x += player_vel

    # w for going up until the border comes up
    if keys[pygame.K_w] and (player.y - player_vel) > 0:  # up
        player.y -= player_vel

    # s for going down until the border comes up
    if keys[pygame.K_s] and (player.y + player_vel + player.get_height() + 15) < HEIGHT:  # down
        player.y += player_vel

    # SPACEBAR for for shooting
    if keys[pygame.K_SPACE]:
        player.shoot()

    # f for exiting
    if keys[pygame.K_f]:
        print("\nThanks for playing xD")
        exit(code=69)


def main():
    # for the game
    run: bool = True
    FPS: int = 60
    level: int = 0
    lives: int = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    # for enemy
    enemies = []
    wave_length = 5
    enemy_vel = 1

    # for player
    player_vel = 5
    laser_vel = 5
    player = Player(300, 630)

    clock = pygame.time.Clock()

    # for counting the total number of times lost
    lost = False
    lost_count = 0

    while run:
        clock.tick(FPS)

        redraw_window(
            main_font=main_font,
            lives=lives,
            level=level,
            enemies=enemies,
            player=player,
            lost=lost,
            lost_font=lost_font
        )

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:  # if all the enemies are killed then
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                # pick a random spawn location and a random color
                enemy = Enemy(
                    random.randrange(50, WIDTH-100),
                    random.randrange(-1500, -100),  # top of the screen
                    random.choice(COLORS)
                )
                enemies.append(enemy)

        # to check whether an user quit or not
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(END_LINE)
                pygame.quit()

        check_keys(player=player, player_vel=player_vel)

        for enemy in enemies:
            enemy.move(enemy_vel)  # the enemy should move down the screen
            # the enemy should shoot laser down the screen
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*FPS) == 1:  # need to have luck in order to shoot
                enemy.shoot()

            if collide(enemy, player):  # if player collides with enemy
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:  # if the enemy reaches the bottem then
                lives -= 1
                enemies.remove(enemy)

        # laser moves upward for it goes in -Y axis
        player.move_lasers(-laser_vel, enemies)


def run():
    title_font = pygame.font.SysFont("comicsans", 70)
    quit_font = pygame.font.SysFont("Castellar", 50)

    while True:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render(
            """Press the mouse to begin...""",
            1,
            (255, 255, 255)
        )
        quit_label = quit_font.render(
            """Press f to quit""",
            1,
            (255, 255, 255)
        )
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        WIN.blit(quit_label, (WIDTH/2 - quit_label.get_width()/2, 550))
        pygame.display.update()

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            # if the user exits then
            if event.type == pygame.QUIT:
                break

            # check whether a mouse buttin is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

            # f for exiting
            if keys[pygame.K_f]:
                print("\nThanks for playing xD")
                exit(code=69)

    print(END_LINE)
    pygame.quit()


if __name__ == "__main__":
    run()
