import sys
import pygame
import time
import numpy as np
from defined_games import get_game
from hero import Hero
from game_menu import show_menu_screen
from colors import BLACK, WHITE, PURPLE, BLUE, ORANGE

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
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
grid_x_start = col_width = grid_y_start = row_height = 0

# pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
# pygame.mixer.music.play(loops=-1)
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
# collision_sound = pygame.mixer.Sound("sfx_exp_short_hard7.wav")
eat_snd = pygame.mixer.Sound("assets/sounds/eat.wav")
wrong_snd = pygame.mixer.Sound("assets/sounds/wrong_answer.wav")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)
clock = pygame.time.Clock()


# Create a custom event for adding a new enemy
# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
# ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)


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

    cell_font_path = pygame.font.match_font("freesans")
    cell_font = pygame.font.Font(cell_font_path, 40)
    for row in range(rows):
        for col in range(cols):
            value = grid[row, col]
            if value == np.iinfo(np.int).max:
                continue
            cell_surf = cell_font.render(str(value), True, WHITE)
            cell_rect = cell_surf.get_rect()

            # calculate centering the number
            cell_pos = (grid_x_start + (col * col_width), grid_y_start + (row * row_height))
            cell_pos = (cell_pos[0] + (col_width - cell_rect.width) / 2,
                        cell_pos[1] + (row_height - cell_rect.height) / 2)

            cell_rect.move_ip(cell_pos)
            screen.blit(cell_surf, cell_rect)


def show_level(scrn, level):
    """Show level on main screen above the game grid"""
    lvl_y = 50
    lvl_x = 20

    _font = pygame.font.SysFont("Courier New", 32)
    _surf = _font.render(f"Level: {level:2}", True, WHITE)
    scrn.blit(_surf, (lvl_x, lvl_y))


def show_title(scrn, title_txt):
    """Show Title above game grid (i.e. Multiples of 2)"""
    thickness = 3
    title_padding = 4
    title_height = 40
    top_y = 40
    bottom_y = top_y + title_height + (4 * title_padding)

    # Get Title and title width to center title
    start_from = scrn.get_width() // 3
    line_w = int(scrn.get_width() // 2)
    top_line = pygame.draw.line(scrn, ORANGE, (start_from, top_y), (start_from + line_w, top_y), thickness)
    bottom_line = pygame.draw.line(scrn, ORANGE, (start_from, bottom_y), (start_from + line_w, bottom_y), thickness)

    _font = pygame.font.SysFont("Courier New", 48)
    _surf = _font.render(title_txt, True, WHITE)
    w = _surf.get_width()
    _x = start_from + ((line_w - w) // 2)
    scrn.blit(_surf, (_x, top_y + title_padding))


def show_score(scrn, score):
    """Show score underneath the game grid."""
    score_txt_y = 500 + grid_y_start + 20
    score_txt_x = 20

    _font = pygame.font.SysFont("Courier New", 36)
    _surf = _font.render("Score:  ", True, WHITE)
    scrn.blit(_surf, (score_txt_x, score_txt_y))

    score_box = _font.render(f"{score:5} ", True, WHITE, BLACK)
    # thickness of border
    border = 4
    bgrnd = pygame.Surface((score_box.get_width() + (2 * border),
                            score_box.get_height() + (2 * border)))
    bgrnd.fill(BLACK)
    rect = bgrnd.get_rect()
    pygame.draw.rect(bgrnd, BLUE, rect, border)

    screen.blit(bgrnd, (score_txt_x + _surf.get_width() - border, score_txt_y - border))
    scrn.blit(score_box, (score_txt_x + _surf.get_width(), score_txt_y))


def show_game_over(scrn):
    _text = pygame.font.Font("assets/fonts/auto_digital.ttf", 76)
    _surf = _text.render("Game Over", True, (255, 0, 0))
    _smtext = pygame.font.Font("assets/fonts/auto_digital.ttf", 32)
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
    pygame.display.update()
    wait_for_any_key()
    show_menu_screen(scrn)

def display_message(msg):
    left = grid_x_start
    top = grid_y_start + 2 * row_height
    bgrnd_width = col_width * 6
    bgrnd_height = row_height
    pygame.display.update()

    bgrnd = pygame.Surface((bgrnd_width, bgrnd_height))
    bgrnd.fill(BLACK)
    rect = bgrnd.get_rect()
    pygame.draw.rect(bgrnd, PURPLE, rect, 2)

    cell_font_path = pygame.font.match_font("freesans")
    cell_font = pygame.font.Font(cell_font_path, 32)
    cell_surf = cell_font.render(str(msg), True, WHITE, BLACK)

    # display black background in middle of grid
    screen.blit(bgrnd, (left, top))
    # display message centered on top of bgrnd
    screen.blit(cell_surf,
                (left + (bgrnd_width - cell_surf.get_width()) / 2, top + (bgrnd_height - cell_surf.get_height()) / 2))
    pygame.display.update()


def display_completed_level():
    for i in range(9):
        screen.fill(BLUE)
        display_message("Good Job!")
        pygame.display.flip()
        clock.tick(9)
        screen.fill(PURPLE)
        display_message("Good Job!")
        pygame.display.flip()
        clock.tick(9)


def wait_for_any_key():
    time.sleep(1)
    waiting = True
    while waiting:

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                waiting = False

    return


def main(lives=3):
    pygame.display.set_caption("MuRrAy MuNcHeRs!")
    chosen_game = show_menu_screen(screen)

    game = get_game(chosen_game)
    game.set_lives(lives)
    grid = game.grid
    draw_grid(screen, grid)

    hero = Hero(display=screen, shape=game.grid.shape)
    # enemies = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    running = True
    while running:

        if game.beat_level():
            display_completed_level()
            game.start_next_level()

        screen.fill(BLACK)
        show_level(screen, game.level)
        show_title(screen, game.level_title)
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == QUIT:
                    running = False
                    sys.exit()

                elif event.key == K_SPACE and game.is_cell_populated(hero.x, hero.y):
                    if game.munch_number(hero.x, hero.y):
                        eat_snd.play()
                    else:
                        wrong_snd.play()
                        show_score(screen, game.score)
                        draw_grid(screen, game.grid)
                        display_message(game.message)
                        if game.gameover is True:
                            running = False
                        wait_for_any_key()

                pressed_keys = pygame.key.get_pressed()
                # Update player based ok keys pressed
                hero.update_position(pressed_keys)

            elif event.type == QUIT:
                running = False

        hero.move()
        screen.blit(hero.surf, hero.rect)
        show_score(screen, game.score)
        draw_grid(screen, game.grid)

        pygame.display.flip()

        # Ensure program maximum rate of 100 fps
        clock.tick(100)

    if game.gameover:
        if game.beat_level():
            print("I did win!!!")
        else:
            show_game_over(screen)


main()

# TODO:
# Show game win screen
# Add Multiples GameType
# Add menu to choose Game Type
# Refactor hard-coded stuff inside hero.py
# Add Enemy
# Add Lives (Like 3 Lives)
# Draw Hero
# Draw Enemy
# Add plumbing
