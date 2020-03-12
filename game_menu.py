"""Build a screen where the player can choose the game that want to play"""
import sys
import pygame
from time import sleep
from defined_games import GameType
from colors import BLACK, WHITE, GREEN


prompt = "Which Game do you want to play?"


def show_menu_screen(scrn):
    screen = scrn
    screen.fill(BLACK)

    _font = pygame.font.SysFont("Courier New", 32)
    _surf = _font.render(prompt, True, WHITE)
    main_top = 50
    main_left = 50
    screen.blit(_surf, (main_left, main_top))

    option_font = pygame.font.SysFont("Courier New", 24)
    option_left = main_left + (main_left // 4)

    for idx, game in enumerate(GameType):
        title = f"{game.value}.  {game.name}"
        option = option_font.render(title, True, WHITE)
        screen.blit(option, (option_left, main_top + (idx + 1) * main_top))

    display_menu = True
    while display_menu:
        pygame.display.update()

        # listen for key to choose number
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.QUIT:
                    display_menu = False
                try:
                    return GameType(event.key - pygame.K_0)
                except ValueError as e:
                    # key pressed was not a GameType
                    pass

    sys.exit()
