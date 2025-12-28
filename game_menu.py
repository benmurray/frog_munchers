"""Build a screen where the player can choose the game that want to play"""
import pygame
import pygame_menu
import settings
from defined_games import GameType
from settings import asset_path


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


bg_image = pygame_menu.BaseImage(
    image_path=str(asset_path("images", "farrar.jpg"))
)


def draw_background(screen):
    bg_image.draw(screen)


def show_menu_screen(screen):
    global display_menu, game_selected
    display_menu = True

    menu_music = pygame.mixer.Sound(str(asset_path("sounds", "menu.ogg")))
    menu_music.play(-1)
    screen = screen

    bg_image.draw(screen)

    my_theme = pygame_menu.Theme(background_color=settings.GREEN2,  # transparent background
                                 title_background_color=settings.GREEN,
                                 title_font_shadow=True,
                                 widget_font=pygame_menu.font.FONT_FRANCHISE,
                                 widget_font_color="#ffffff",
                                 title_font_color="#ffffff",
                                 widget_padding=25,
                                 )
    my_theme.set_background_color_opacity(0.7)

    menu = pygame_menu.Menu(f'{settings.TITLE}',
                            width=screen.get_width() * 0.6,
                            height=screen.get_height() * 0.7,
                            theme=my_theme)

    while display_menu:
        menu.add.selector('Game Type:', GAME_TYPES, onchange=set_game_type)
        menu.add.button('Play', start_game, menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        draw_background_func = lambda: draw_background(screen)
        menu.mainloop(screen, draw_background_func)
        pygame.display.update()
    menu_music.stop()
    return GameType(game_selected)
