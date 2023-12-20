import sys
import os
import pygame
import time
import numpy as np

from EnemyManager import EnemyManager
from defined_games import get_game, GameType
from hero import Hero
from game_menu import show_menu_screen
from colors import BLACK, WHITE, PURPLE, BLUE, ORANGE

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, GREEN, TITLE

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

grid_x_start = col_width = grid_y_start = row_height = 0

eat_snd = pygame.mixer.Sound("assets/sounds/eat.ogg")
wrong_snd = pygame.mixer.Sound("assets/sounds/wrong_answer.wav")
ambient_music = pygame.mixer.Sound("assets/sounds/ambient.ogg")
complete_level_fanfare = pygame.mixer.Sound("assets/sounds/tadah.ogg")
gameover_music = pygame.mixer.Sound("assets/sounds/gameover.ogg")
win_snd = pygame.mixer.Sound("assets/sounds/fanfare.wav")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(GREEN)
clock = pygame.time.Clock()


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


def draw_offstage(screen: pygame.Surface) -> None:
    """
    Draws a black rectangle around the grid. Used to hide enemies spawning off grid and coming
    into the grid.
    """
    global grid_x_start, grid_y_start
    width = 900
    height = 500  # These need to be the same as in draw_grid (for now)
    screen_width = int(screen.get_width())
    screen_height = int(screen.get_height())
    top = pygame.Surface((screen_width, grid_y_start))
    bottom = pygame.Surface((screen_width, grid_y_start))
    left = pygame.Surface((grid_x_start, screen_height))
    right = pygame.Surface((grid_x_start, screen_height))

    screen.blit(top, dest=(0, 0))
    screen.blit(bottom, dest=(0, screen_height - grid_y_start))
    screen.blit(left, dest=(0, 0))
    screen.blit(right, dest=(screen_width - (screen_width - width) / 2, 0))


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


def show_lives(screen, num_lives=3):
    """ Lives: @@@ """
    hero_image = pygame.image.load('assets/images/life_indicator.png').convert()
    width = hero_image.get_width()
    width += 5  # add space between each individual image
    lives_surface = pygame.Surface((width * 3, 50))

    for i in range(num_lives):
        lives_surface.blit(hero_image, dest=(width * i, 0), area=(0, 0, width, 50))

    text = "Lives: "
    font = pygame.font.SysFont("Courier New", 32)
    text_surface = font.render(text, True, WHITE)

    w = screen.get_width()
    h = screen.get_height()

    h = h - lives_surface.get_height();
    w = w - (text_surface.get_width() + lives_surface.get_width())

    screen.blit(text_surface, dest=(w, h))
    screen.blit(lives_surface, dest=(w + text_surface.get_width(), h))


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


def show_game_win(scrn, score):
    show_game_over(scrn, won=True, score=score)


def show_game_over(scrn, won=False, score=0):
    ambient_music.stop()
    scrn.fill((0, 0, 0))

    text_font_32 = pygame.font.Font("assets/fonts/auto_digital.ttf", 32)
    text_font_64 = pygame.font.Font("assets/fonts/auto_digital.ttf", 64)
    if won:
        title_text = text_font_64.render("You Win", True, (255, 0, 0))
    else:
        title_text = text_font_64.render("Game Over", True, (255, 0, 0))

    score = text_font_64.render(f"Score = {score}", True, (255, 0, 0))
    score_rect = score.get_rect()

    text_font = pygame.font.Font("assets/fonts/auto_digital.ttf", 32)
    instructions_text = text_font_32.render("Press (any key) to Continue", True, (255, 0, 0))

    title_text_rect = title_text.get_rect()
    instructions_rect = instructions_text.get_rect()

    _center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    title_text_rect.move_ip(_center[0] - (title_text.get_width() / 2),
                            _center[1] - (title_text.get_height() / 2))
    if won:
        # move title text up a bit
        title_text_rect.move_ip(0, -100)
        score_rect.move_ip(_center[0] - (score.get_width() / 2), _center[1])
        instructions_rect.move_ip(_center[0] - (instructions_text.get_width() / 2), _center[1] + 200)
        scrn.blit(score, score_rect)
        win_snd.play()
    else:
        instructions_rect.move_ip(_center[0] - (instructions_text.get_width() / 2), _center[1] + 100)
        gameover_music.play(-1)

    scrn.blit(title_text, title_text_rect)
    scrn.blit(instructions_text, instructions_rect)
    pygame.display.flip()
    pygame.display.update()
    wait_for_any_key()
    gameover_music.stop()
    win_snd.stop()


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
    ambient_music.stop()
    complete_level_fanfare.play()
    for i in range(9):
        screen.fill(BLUE)
        display_message("Good Job!")
        pygame.display.flip()
        clock.tick(9)
        screen.fill(PURPLE)
        display_message("Good Job!")
        pygame.display.flip()
        clock.tick(9)
    ambient_music.play()


def wait_for_any_key():
    time.sleep(1)
    waiting = True
    while waiting:

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                waiting = False

    return


def run_game_loop(chosen_game, lives=3, level=None):
    game = get_game(chosen_game)
    if level is None:
        game.start_over(lives)
    else:
        game.start_over(lives, level)
    grid = game.grid
    draw_grid(screen, grid)

    hero = Hero(display=screen, shape=game.grid.shape, game=game)
    enemy_manager = EnemyManager(screen=screen)
    # enemies = pygame.sprite.Group()

    ambient_music.play(-1).set_volume(0.75)
    eat_snd.set_volume(0.3)
    time_at_level_start = pygame.time.get_ticks()
    running = True
    while running:

        if game.beat_level():
            display_completed_level()
            game.start_next_level()
            enemy_manager.level = game.level

        screen.fill(BLACK)
        # pressed_keys
        for event in pygame.event.get():

            pressed_keys = pygame.key.get_pressed()

            # Quit at anytime with shift + escape
            if pressed_keys[pygame.K_ESCAPE] and (pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]):
                pygame.display.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE and game.is_cell_populated(hero.x, hero.y):
                    if game.munch_number(hero.x, hero.y):
                        eat_snd.play()
                    else:
                        wrong_snd.play()
                        show_score(screen, game.score)
                        draw_grid(screen, game.grid)
                        display_message(game.message)
                        if game.gameover is True:
                            running = False

                # Update player based ok keys pressed
                hero.update_position(pressed_keys)

            elif event.type == QUIT:
                ambient_music.stop()
                running = False

        hero.update()
        enemy_manager.update()

        screen.blit(hero.surf, hero.rect)

        draw_grid(screen, game.grid)
        draw_offstage(screen)
        show_level(screen, game.level)
        show_title(screen, game.level_title)
        show_score(screen, game.score)
        show_lives(screen, game.lives)

        pygame.display.flip()

        # Ensure program maximum rate of 100 fps
        clock.tick(FRAME_RATE)

        if game.gameover:
            running = False
            ambient_music.stop()
            if game.beat_level():
                show_game_win(screen, game.score)
            else:
                show_game_over(screen)
        elif not running:
            pygame.display.quit()
            sys.exit()


def start_game():
    pygame.display.set_caption(TITLE)
    while True:
        if os.getenv('TESTING_MUNCHER') == '1':
            run_game_loop(GameType.Multiples, lives=1, level=11)
        else:
            chosen_game = show_menu_screen(screen)
            run_game_loop(chosen_game)


start_game()

# Add Enemy
"""
Determine types - randome, straight line, 80% follow muncher
How many to put in each level
How to enter and leave grid
Develop simple AI for them
"""
