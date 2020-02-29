import sys
import pygame
import random
import numpy as np
import enum
from time import sleep
from defined_games import Evens

from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_q,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (180, 0, 180)
GREEN = (0, 255, 0)


class GameType(enum.Enum):
    odds = 1
    evens = 2
    multiples = 3
    factors = 4


pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
grid_x_start = col_width = grid_y_start = row_height = 0

# pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
# pygame.mixer.music.play(loops=-1)
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
# collision_sound = pygame.mixer.Sound("sfx_exp_short_hard7.wav")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)

current_score = 0
clock = pygame.time.Clock()


# Create a custom event for adding a new enemy
# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
# ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)


def get_game_type(game="Evens", level=1):
    return Evens(level=level)


def draw_grid(screen, grid):
    """Draw a 5x6 grid"""
    global grid_x_start, col_width, grid_y_start, row_height
    rows, cols = grid.shape
    line_width = 3
    width = 900
    height = 500
    grid_x_start = (SCREEN_WIDTH - width) / 2
    col_width = int(width / cols)
    grid_y_start = (SCREEN_HEIGHT - height) / 2
    row_height = int(height / rows)
    # outside = pygame.rect(left=20, top=20, width=800, height=600)
    pygame.draw.rect(screen, PURPLE, (grid_x_start, grid_y_start, width, height), line_width)
    for row in range(1, rows):
        pygame.draw.line(screen, PURPLE, (grid_x_start, grid_y_start + (row_height * row)),
                         (grid_x_start + width, grid_y_start + (row_height * row)), line_width)
    for col in range(1, cols):
        pygame.draw.line(screen, PURPLE, (grid_x_start + (col_width * col), grid_y_start),
                         (grid_x_start + (col_width * col), grid_y_start + height), line_width)

    cell_font = pygame.font.Font("/usr/share/fonts/truetype/tlwg/TlwgTypewriter.ttf", 40)
    for row in range(rows):
        for col in range(cols):
            value = grid[row, col]
            if value < 0:
                continue
            cell_surf = cell_font.render(str(value), True, WHITE)
            cell_rect = cell_surf.get_rect()

            # calculate centering the number
            cell_pos = (grid_x_start + (col * col_width), grid_y_start + (row * row_height))
            cell_pos = (cell_pos[0] + (col_width - cell_rect.width) / 2,
                        cell_pos[1] + (row_height - cell_rect.height) / 2)

            cell_rect.move_ip(cell_pos)
            screen.blit(cell_surf, cell_rect)


def reset_game():
    global current_score
    # pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
    # pygame.mixer.music.play(loops=-1)
    current_score = 0


def show_game_over(scrn):
    _text = pygame.font.Font("/home/ben/.local/share/fonts/auto_digital.ttf", 76)
    _surf = _text.render("Game Over", True, (255, 0, 0))
    _smtext = pygame.font.Font("/home/ben/.local/share/fonts/auto_digital.ttf", 32)
    _qinstr = _smtext.render("Press (any key) to Quit", True, (255, 0, 0))
    _rect = _surf.get_rect()
    _qrect = _qinstr.get_rect()
    _center = (
        (SCREEN_WIDTH - _surf.get_width()) / 2,
        (SCREEN_HEIGHT - _surf.get_height()) / 2
    )
    _rect.move_ip(_center)
    _qrect.move_ip(_center[0], _center[1] + 100)
    scrn.fill((0, 0, 0))
    scrn.blit(_surf, _rect)
    scrn.blit(_qinstr, _qrect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pygame.quit()
                sys.exit()


class Hero(pygame.sprite.Sprite):
    def __init__(self, display=screen, shape=(5, 6)):
        super(Hero, self).__init__()
        self.surf = pygame.Surface((80, 80))
        self.rect = self.surf.get_rect()
        self.surf.fill(GREEN)
        self.screen = display
        self.grid = np.zeros(shape=shape)
        self.x = shape[1] // 2
        self.y = shape[0] // 2
        self.rect.left = grid_x_start + (self.x * col_width) + (col_width - self.rect.w) // 2
        self.rect.top = grid_y_start + (self.y * row_height) + (row_height - self.rect.h) // 2

    def update_position(self, pressed_keys):
        delta_x, delta_y = 0, 0
        if pressed_keys[pygame.K_UP]:
            delta_y = -1
        if pressed_keys[pygame.K_DOWN]:
            delta_y = 1
        if pressed_keys[pygame.K_LEFT]:
            delta_x = -1
        if pressed_keys[pygame.K_RIGHT]:
            delta_x = 1

        # Keep player on the screen
        if (self.x + delta_x) < 0:
            delta_x = 0
        if (self.x + delta_x) >= self.grid.shape[1]:
            delta_x = 0
        if (self.y + delta_y) < 0:
            delta_y = 0
        if (self.y + delta_y) >= self.grid.shape[0]:
            delta_y = 0

        self.move_to(delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y

    def move_to(self, x, y):
        _x = x * col_width
        _y = y * row_height
        self.rect.move_ip(_x, _y)


def generate_grid(game_type=GameType.evens, level=1, rows_cols=(5, 6)):
    if game_type == GameType.odds or game_type == GameType.evens:
        return generate_odds_or_evens_grid(level, rows_cols)
    else:
        return np.random.randint(100, size=rows_cols)


def generate_odds_or_evens_grid(level=1, grid_size=(5, 6)):
    low = 0
    high = (10 * level) + 1
    return np.random.randint(low, high, size=grid_size)


def munch_number(game_type, hero, grid):
    game_over = False
    cell_value = grid[hero.y, hero.x]
    grid[hero.y, hero.x] = -1
    msg = ""
    if game_type == GameType.odds:
        if cell_value % 2 == 0:
            game_over = True
            msg = f"Look again! {cell_value} is not an odd number."
    elif game_type == GameType.evens:
        if cell_value % 2 == 1:
            game_over = True
            msg = f"Look again! {cell_value} is not an even number."

    return game_over, msg


def display_error_message(msg):
    left = grid_x_start
    top = grid_y_start + 2 * row_height
    bgrnd_width = col_width * 6
    bgrnd_height = row_height
    pygame.display.update()

    bgrnd = pygame.Surface((bgrnd_width, bgrnd_height))
    bgrnd.fill(BLACK)
    rect = bgrnd.get_rect()
    pygame.draw.rect(bgrnd, PURPLE, rect, 2)

    cell_font = pygame.font.Font("/usr/share/fonts/truetype/tlwg/TlwgTypewriter.ttf", 32)
    cell_surf = cell_font.render(str(msg), True, WHITE, BLACK)

    # display black background in middle of grid
    screen.blit(bgrnd, (left, top))
    # display message centered on top of bgrnd
    screen.blit(cell_surf, (left + (bgrnd_width - cell_surf.get_width()) / 2, top + (bgrnd_height - cell_surf.get_height()) / 2))
    pygame.display.update()


def main():
    game_over = False
    msg = ""
    pygame.display.set_caption("MuRrAy MuNcHeRs!")

    # Hard code Level 5 evens
    level = 5
    game_type = GameType.evens
    grid = generate_grid(game_type, level)
    draw_grid(screen, grid)

    hero = Hero()
    # enemies = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    game_over, msg = munch_number(game_type, hero, grid)
                    if game_over:
                        running = False

                pressed_keys = pygame.key.get_pressed()
                # Update player based ok keys pressed
                hero.update_position(pressed_keys)

            elif event.type == QUIT:
                running = False

        screen.blit(hero.surf, hero.rect)
        draw_grid(screen, grid)

        pygame.display.flip()

        # Ensure program maintains a rate of 30 fps
        clock.tick(20)
        # Wait for user to press any key to continue

    if game_over:
        display_error_message(msg)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return
    show_game_over(screen)


main()


# TODO:
# check for win condidtions
# Create GameType class
