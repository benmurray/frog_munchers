"""Build a screen where the player can choose the game that want to play"""
import sys
import pygame
import pygame_menu
from defined_games import GameType
from colors import BLACK, WHITE, GREEN


GAME_TYPES = [('Evens', GameType.Evens), ('Odds', GameType.Odds), ('All Multiples', GameType.Multiples)]
display_menu = True
game_selected = GameType.Evens


def set_game_type(game_type, pos):
    global game_selected
    game_selected = pos


def start_game(menu):
    global display_menu
    display_menu = False
    menu.disable()


def show_menu_screen(screen):
    global display_menu, game_selected

    menu_music = pygame.mixer.Sound("assets/sounds/menu.ogg")
    menu_music.play(-1)

    screen = screen

    menu = pygame_menu.Menu('Welcome to Farrar Muncher', 800, 600,
                            theme=pygame_menu.themes.THEME_GREEN)

    while display_menu:
        menu.add.selector('Game Type:', GAME_TYPES, onchange=set_game_type)
        menu.add.button('Play', start_game, menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(screen)
        pygame.display.update()
    menu_music.stop()
    return GameType(game_selected)
