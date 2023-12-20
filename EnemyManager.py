import pygame
import settings
from enemy import Enemy


class EnemyManager:

    def __init__(self, screen, level: int = 1):
        assert(screen is not None)
        self.screen = screen
        self.current_level = level
        self.start_time = 0
        self.current_level_start_time = 0

        self.enemies = []

    @property
    def level(self):
        return self.current_level

    @level.setter
    def level(self, level: int) -> None:
        self.current_level = level
        self.reset_level()

    # Called once per frame
    def update(self):
        self._check_if_spawn()
        self._update_enemies()

    def clear_enemies(self):
        self.enemies = []

    def _check_if_spawn(self):
        if self.current_level > 0:
            if self._time_to_spawn():
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

    def _time_to_spawn(self) -> bool:
        if len(self.enemies) < 1 and (pygame.time.get_ticks() - self.current_level_start_time < 2000):
            return True
        else:
            return False

    def reset_level(self) -> None:
        """Reset level enemies, level_start_time"""
        self.current_level_start_time = pygame.time.get_ticks()
        self.enemies = []

