'''Enemies
- appear by entering a perimeter square
- move at a specified time interval
- determine where they are going next

 - Levels determine
    - What level an enemy can enter
    - What time on that level they can enter
    - If more than one enemy can appear
    - The types of enemies allowed


    THIS HASN"T BEEN TESTED AT ALL
'''
import pygame
import settings
import numpy as np
from settings import Direction


class Enemy(pygame.sprite.Sprite):
    FRAME_DELTA = 0.12

    def __init__(self, color='purple', shape=(5, 6)):
        print("Enemy Spawned")

        super().__init__()
        self.sprite_sheet = pygame.image.load(f'assets/images/{color}_ghost.png').convert()
        self.image = pygame.Surface((125, 125))
        self.image.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))

        self.idle, self.left, self.right, self.up, self.down = self.create_loops()
        self.current_sprite_loop = self.idle

        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

        self.frame_num = 0
        self.frame_delta = Enemy.FRAME_DELTA

        self.grid = np.zeros(shape=shape)
        self.x = shape[1] // 2
        self.y = shape[0] // 2

        width = settings.BOARD_WIDTH
        height = settings.BOARD_HEIGHT
        grid_x_start = (settings.SCREEN_WIDTH - width) / 2
        col_width = int(width / self.grid.shape[1])
        grid_y_start = (settings.SCREEN_HEIGHT - height) / 2
        row_height = int(height / self.grid.shape[0])

        self.moving = False  # movement across game board
        self.col_width = col_width
        self.row_height = row_height

        self.rect.left = grid_x_start + (self.x * col_width) + (col_width - self.rect.w) // 2
        self.rect.top = grid_y_start + (self.y * row_height) + (row_height - self.rect.h) // 2

        # start off screen
        self.curr_x, self.curr_y = -1000, -1000
        self.curr_x, self.curr_y = 0, 0
        self.dest_x, self.dest_y = self.curr_x, self.curr_y
        self.delta_x = self.delta_y = 0

    def create_loops(self):
        front1 = pygame.Surface((125, 125))
        front1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))
        front2 = pygame.Surface((125, 125))
        front2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 0, 250, 125))
        front3 = pygame.Surface((125, 125))
        front3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 0, 375, 375))
        front2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 0, 250, 125))
        front_loop = [front1, front2, front3, front2]

        left1 = pygame.Surface((125, 125))
        left1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 125, 125, 125))
        left2 = pygame.Surface((125, 125))
        left2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 125, 250, 125))
        left3 = pygame.Surface((125, 125))
        left3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 125, 375, 375))
        left2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 125, 250, 125))
        left_loop = [left1, left2, left3, left2]

        right1 = pygame.Surface((125, 125))
        right1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 250, 125, 125))
        right2 = pygame.Surface((125, 125))
        right2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 250, 250, 125))
        right3 = pygame.Surface((125, 125))
        right3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 250, 375, 375))
        right2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 250, 250, 125))
        right_loop = [right1, right2, right3, right2]

        up1 = pygame.Surface((125, 125))
        up1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 375, 125, 125))
        up2 = pygame.Surface((125, 125))
        up2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 375, 250, 125))
        up3 = pygame.Surface((125, 125))
        up3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 375, 375, 375))
        up2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 375, 250, 125))
        up_loop = [up1, up2, up3, up2]

        return front_loop, left_loop, right_loop, up_loop, front_loop

    def update(self):
        '''Called each iteration of game loop. Loops through sprites of 'self.current_sprite_loop'. '''
        self.frame_num += self.frame_delta
        if self.frame_num >= len(self.current_sprite_loop):
            self.frame_num = 0

        self.image = pygame.transform.scale(self.current_sprite_loop[int(self.frame_num)], (125, 125))

    def update_position(self, direction):
        if self.moving:
            return
        else:
            self.moving = True

        delta_x, delta_y = 0, 0
        if direction == Direction.UP:
            delta_y = -1
        if direction == Direction.DOWN:
            delta_y = 1
        if direction == Direction.LEFT:
            delta_x = -1
        if direction == Direction.RIGHT:
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


