import pygame
import numpy as np

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GREEN = (0, 255, 0)


class Hero(pygame.sprite.Sprite):
    def __init__(self, display, shape=(5, 6)):
        super(Hero, self).__init__()
        hero_sprites = pygame.image.load('hero_sprite.png').convert()
        hero = pygame.Surface((115, 100))
        hero.blit(hero_sprites, dest=(0, 0), area=(0, 301, 115, 100))
        self.surf = pygame.transform.scale(hero, (85, 80))
        self.rect = self.surf.get_rect()
        self.screen = display
        self.grid = np.zeros(shape=shape)
        self.x = shape[1] // 2
        self.y = shape[0] // 2

        # TODO Get rid of this and pass it in or something
        width = 900
        height = 500
        grid_x_start = (SCREEN_WIDTH - width) / 2
        col_width = int(width / self.grid.shape[1])
        grid_y_start = (SCREEN_HEIGHT - height) / 2
        row_height = int(height / self.grid.shape[0])

        self.col_width = col_width
        self.row_height = row_height

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
        _x = x * self.col_width
        _y = y * self.row_height
        self.rect.move_ip(_x, _y)
