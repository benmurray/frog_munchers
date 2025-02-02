import time
import pygame
import settings
from enemy import Enemy


class EnemyManager:

    def __init__(self, screen, level: int = 1):
        assert(screen is not None)
        self.screen = screen
        self.max_enemies_at_level = 0
        self.start_time = 0
        self.current_level_start_time = 0
        self.last_spawn_time = 0
        self.cool_down_time = 3

        self.enemies = []
        if level is None:
            self.level = 1
        else:
            self.level = level

    @property
    def level(self):
        return self.current_level

    @level.setter
    def level(self, level: int) -> None:
        self.current_level = level
        self.reset_level()

    # Called once per frame
    def update(self, time_in_level: int = 0):
        self._check_if_spawn(time_in_level)
        self._update_enemies()

    def clear_enemies(self):
        self.enemies = []

    def _check_if_spawn(self, time_in_level):
        """_summary_

        Args:
            time_in_level (int): time, in seconds, of being in level
        """
        if self.current_level > 0:
            if self._time_to_spawn(time_in_level):
                new_enemy = Enemy()
                self.enemies.append(new_enemy)
                # spawn enemy
                start_x = (settings.SCREEN_WIDTH - settings.BOARD_WIDTH) / 2
                start_y = (settings.SCREEN_HEIGHT - settings.BOARD_HEIGHT) / 2

                # have it spawn to left of first grid cell TODO: Make this dynamic
                start_x -= 125
                new_enemy.rect.move_ip(start_x, start_y)

    def _update_enemies(self):
        for enemy in self.enemies:
            enemy.update()

    def _time_to_spawn(self, time_in_level) -> bool:
        in_cool_down = (time_in_level - self.last_spawn_time) > self.cool_down_time

        if in_cool_down and len(self.enemies) < self.max_enemies_at_level:
            self.last_spawn_time = time_in_level
            return True
        else:
            return False

    def reset_level(self) -> None:
        """Reset level enemies, level_start_time"""
        self.max_enemies_at_level = self.current_level // 3
        self.enemies = []
