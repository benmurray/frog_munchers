import pygame
import numpy as np

import settings

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GREEN = (0, 255, 0)


class Hero(pygame.sprite.Sprite):

    def __init__(self, display, shape=(5, 6), game=None):
        super(Hero, self).__init__()
        self.build_images()
        self.moving = False
        self.move_count = 0
        self.game = game

        self.surf = pygame.transform.scale(self.mouth_open, (85, 80))

        self.rect = self.surf.get_rect()
        self.screen = display
        self.grid = np.zeros(shape=shape)
        self.x = shape[1] // 2
        self.y = shape[0] // 2

        width = settings.BOARD_WIDTH
        height = settings.BOARD_HEIGHT
        grid_x_start = (SCREEN_WIDTH - width) / 2
        col_width = int(width / self.grid.shape[1])
        grid_y_start = (SCREEN_HEIGHT - height) / 2
        row_height = int(height / self.grid.shape[0])

        self.col_width = col_width
        self.row_height = row_height

        self.rect.left = grid_x_start + (self.x * col_width) + (col_width - self.rect.w) // 2
        self.rect.top = grid_y_start + (self.y * row_height) + (row_height - self.rect.h) // 2
        self.curr_x, self.curr_y = self.get_start_x_y()
        self.dest_x, self.dest_y = self.curr_x, self.curr_y
        self.delta_x = self.delta_y = 0

    def build_images(self):
        hero_sprites = pygame.image.load('assets/images/hero_sprite.png').convert()
        self.standing_hero = pygame.Surface((115, 100))
        self.standing_hero.blit(hero_sprites, dest=(0, 0), area=(0, 0, 115, 100))

        self.moving_right1 = pygame.Surface((115, 100))
        self.moving_right1.blit(hero_sprites, dest=(0, 0), area=(0, 101, 115, 100))

        self.moving_right2 = pygame.Surface((115, 100))
        self.moving_right2.blit(hero_sprites, dest=(0, 0), area=(0, 201, 115, 100))

        self.mouth_open = pygame.Surface((115, 100))
        self.mouth_open.blit(hero_sprites, dest=(0, 0), area=(0, 301, 115, 100))

        self.scared = pygame.Surface((115, 100))
        self.scared.blit(hero_sprites, dest=(0, 0), area=(0, 401, 115, 100))

    def close_mouth(self):
        self.surf = pygame.transform.scale(self.standing_hero, (85, 80))

    def open_mouth(self):
        self.surf = pygame.transform.scale(self.mouth_open, (85, 80))

    def move_one(self):
        self.surf = pygame.transform.scale(self.moving_right1, (85, 80))

    def move_two(self):
        self.surf = pygame.transform.scale(self.moving_right2, (85, 80))

    def update_position(self, pressed_keys):
        if self.moving:
            return
        else:
            self.moving = True

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

        self.set_destination(delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y
        self.delta_x = delta_x
        self.delta_y = delta_y

    def get_start_x_y(self):
        return self.x * self.col_width, self.y * self.row_height

    def set_destination(self, x, y):
        self.dest_x = x * self.col_width + self.curr_x
        self.dest_y = y * self.row_height + self.curr_y

    def move(self):
        if self.delta_x == 0 and self.delta_y == 0:
            self.moving = False
            self.move_count = 0
            if self.game.is_cell_populated(self.x, self.y):
                self.open_mouth()
            else:
                self.close_mouth()
        else:
            self.move_count += 1

            if self.move_count % 3 == 0:
                if self.move_count % 6 == 0:
                    self.move_two()
                else:
                    self.move_one()

        move_step = 10
        if self.delta_x > 0:
            if self.curr_x >= self.dest_x:
                self.curr_x = self.dest_x
                self.delta_x = 0
                return
        if self.delta_x < 0:
            if self.curr_x <= self.dest_x:
                self.curr_x = self.dest_x
                self.delta_x = 0
                return
        if self.delta_y > 0:
            if self.curr_y >= self.dest_y:
                self.curr_y = self.dest_y
                self.delta_y = 0
                return
        if self.delta_y < 0:
            if self.curr_y <= self.dest_y:
                self.curr_y = self.dest_y
                self.delta_y = 0
                return
        move_x = move_y = 0

        if self.delta_x > 0 and self.curr_x < self.dest_x:
            self.curr_x += move_step
            move_x = move_step
        elif self.delta_x < 0 and self.curr_x > self.dest_x:
            self.curr_x -= move_step
            move_x = -move_step

        if self.delta_y > 0 and self.curr_y < self.dest_y:
            self.curr_y += move_step
            move_y = move_step
        elif self.delta_y and self.curr_y > self.dest_y:
            self.curr_y -= move_step
            move_y = -move_step

        self.rect.move_ip(move_x, move_y)
