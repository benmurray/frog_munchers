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
import random
from typing import List, Optional, Tuple

import pygame
import settings
import numpy as np
from settings import Direction


class Enemy(pygame.sprite.Sprite):
    FRAME_DELTA = 0.12
    SPAWN_FADE_DURATION = 0.1  # seconds
    MOVE_DURATION = 1.0  # seconds to move between cells (slightly slower)

    def __init__(self, color: str = 'purple', shape: Tuple[int, int] = (5, 6)) -> None:
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'assets/images/{color}_ghost.png').convert_alpha()
        self.image = pygame.Surface((125, 125))
        self.image.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))

        self.idle, self.left, self.right, self.up, self.down = self.create_loops()
        self.current_sprite_loop = self.idle

        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.hitbox = self.rect.inflate(-40, -40)

        self.frame_num = 0
        self.frame_delta = Enemy.FRAME_DELTA

        self.grid = np.zeros(shape=shape)
        self.x = shape[1] // 2
        self.y = shape[0] // 2

        width = settings.BOARD_WIDTH
        height = settings.BOARD_HEIGHT
        self.grid_x_start = (settings.SCREEN_WIDTH - width) / 2
        self.col_width = int(width / self.grid.shape[1])
        self.grid_y_start = (settings.SCREEN_HEIGHT - height) / 2
        self.row_height = int(height / self.grid.shape[0])

        self.moving = False  # movement across game board

        self.rect.left = (
            self.grid_x_start + (self.x * self.col_width) + (self.col_width - self.rect.w) // 2
        )
        self.rect.top = (
            self.grid_y_start + (self.y * self.row_height) + (self.row_height - self.rect.h) // 2
        )
        self._sync_hitbox()

        # start off screen
        self.curr_x, self.curr_y = -1000, -1000
        self.curr_x, self.curr_y = 0, 0
        self.dest_x, self.dest_y = self.curr_x, self.curr_y
        self.delta_x = self.delta_y = 0
        self.spawn_time = 0  # when the enemy visually appears on grid
        self.entry_time = 0  # scheduled time to enter the grid
        self.entered = False
        self.next_move_at = 0
        self.moving = False
        self.leaving = False
        self.has_left_grid = False
        self.move_start_time = 0.0
        self.move_start_pos = (0.0, 0.0)
        self.move_dest_pos = (0.0, 0.0)
        self.move_dest_cell = (self.y, self.x)

    def create_loops(self) -> Tuple[List[pygame.Surface], List[pygame.Surface], List[pygame.Surface], List[pygame.Surface], List[pygame.Surface]]:
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

    def update(self, current_time_sec: float) -> None:
        """Called each iteration of game loop."""
        self.frame_num += self.frame_delta
        if self.frame_num >= len(self.current_sprite_loop):
            self.frame_num = 0

        self.image = pygame.transform.scale(self.current_sprite_loop[int(self.frame_num)], (125, 125))
        self._update_move(current_time_sec)

    def update_position(self, direction: Direction) -> None:
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

    def set_destination(self, x: int, y: int) -> None:
        self.dest_x = x * self.col_width + self.curr_x
        self.dest_y = y * self.row_height + self.curr_y

    def move(self) -> None:
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

    def set_grid_position(self, row: int, col: int) -> None:
        """Place the enemy at a given grid cell (row, col)."""
        self.set_position_at_cell(row=row, col=col)

    def set_position_at_cell(self, row: int, col: int) -> None:
        """Place the enemy at a given cell coordinate (can be off-grid for entry/exit)."""
        self.x = col
        self.y = row
        self.rect.left = (
            self.grid_x_start + (col * self.col_width) + (self.col_width - self.rect.w) // 2
        )
        self.rect.top = (
            self.grid_y_start + (row * self.row_height) + (self.row_height - self.rect.h) // 2
        )
        self.curr_x, self.curr_y = self.rect.left, self.rect.top
        self.dest_x, self.dest_y = self.curr_x, self.curr_y
        self._sync_hitbox()

    def apply_fade(self, current_time_sec: float) -> None:
        """Fade in based on time since spawn."""
        if not self.entered:
            return
        elapsed = max(0.0, current_time_sec - self.spawn_time)
        progress = min(1.0, elapsed / Enemy.SPAWN_FADE_DURATION)
        alpha = int(255 * progress)
        self.image.set_alpha(alpha)

    def schedule_next_move(self, now_sec: float) -> None:
        """Pick a random interval between 2-5 seconds for the next move."""
        self.next_move_at = now_sec + random.uniform(2, 5)

    def pick_adjacent_or_leave(self) -> Optional[Tuple[int, int, bool]]:
        """Choose a random orthogonally adjacent cell; allow leaving when on perimeter."""
        rows, cols = self.grid.shape
        options = []
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in deltas:
            nr, nc = self.y + dy, self.x + dx
            if 0 <= nr < rows and 0 <= nc < cols:
                options.append((nr, nc, False))
        leave_targets = []
        if self.x == 0:
            leave_targets.append((self.y, -1))
        if self.x == cols - 1:
            leave_targets.append((self.y, cols))
        if self.y == 0:
            leave_targets.append((-1, self.x))
        if self.y == rows - 1:
            leave_targets.append((rows, self.x))
        for lr, lc in leave_targets:
            options.append((lr, lc, True))
        if not options:
            return None
        return random.choice(options)

    def move_adjacent_or_leave(self, now_sec: float) -> Optional[bool]:
        """Move to an orthogonally adjacent cell within the grid."""
        dest = self.pick_adjacent_or_leave()
        if dest is None:
            return None
        row, col, leaving = dest
        return self._start_move(dest_row=row, dest_col=col, now_sec=now_sec, leaving=leaving)

    def _start_move(self, dest_row: int, dest_col: int, now_sec: float, leaving: bool = False) -> bool:
        """Begin animating a move to a destination cell."""
        self.moving = True
        self.leaving = leaving
        self.has_left_grid = False
        self.move_start_time = now_sec
        self.move_start_pos = (float(self.rect.left), float(self.rect.top))
        self.move_dest_cell = (dest_row, dest_col)
        self.move_dest_pos = (
            self.grid_x_start + (dest_col * self.col_width) + (self.col_width - self.rect.w) // 2,
            self.grid_y_start + (dest_row * self.row_height) + (self.row_height - self.rect.h) // 2,
        )
        self._set_direction_loop(dest_row, dest_col)
        return True

    def _update_move(self, current_time_sec: float) -> None:
        """Interpolate movement if currently moving."""
        if not self.moving:
            return
        elapsed = current_time_sec - self.move_start_time
        progress = max(0.0, min(1.0, elapsed / Enemy.MOVE_DURATION))
        start_x, start_y = self.move_start_pos
        dest_x, dest_y = self.move_dest_pos
        new_x = start_x + (dest_x - start_x) * progress
        new_y = start_y + (dest_y - start_y) * progress
        self.rect.left = int(new_x)
        self.rect.top = int(new_y)
        self._sync_hitbox()
        if progress >= 1.0:
            # Snap to cell and finish
            row, col = self.move_dest_cell
            rows, cols = self.grid.shape
            if self.leaving and (row < 0 or row >= rows or col < 0 or col >= cols):
                # Completed leaving the grid
                self.rect.left = int(dest_x)
                self.rect.top = int(dest_y)
                self._sync_hitbox()
                self.has_left_grid = True
            else:
                self.set_grid_position(row=row, col=col)
            self.moving = False
            self.leaving = False
            self.current_sprite_loop = self.idle

    def _set_direction_loop(self, dest_row: int, dest_col: int) -> None:
        """Switch sprite loop based on intended move direction."""
        if dest_col < self.x:
            self.current_sprite_loop = self.left
        elif dest_col > self.x:
            self.current_sprite_loop = self.right
        elif dest_row < self.y:
            self.current_sprite_loop = self.up
        elif dest_row > self.y:
            self.current_sprite_loop = self.down
        else:
            self.current_sprite_loop = self.idle

    def _sync_hitbox(self) -> None:
        """Keep hitbox aligned and slightly smaller than the sprite rect."""
        self.hitbox = self.rect.inflate(-40, -40)
