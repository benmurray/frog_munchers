from typing import List, Tuple

import pygame
import settings
import random
from enemy import Enemy


class EnemyManager:

    def __init__(self, screen: pygame.Surface, level: int = 1, grid_shape: Tuple[int, int] = (5, 6)) -> None:
        assert(screen is not None)
        self.screen = screen
        self.spawn_rules = settings.ENEMY_SPAWN_RULES
        self.grid_shape = grid_shape
        self.entry_delay_range = (0, 0)
        self.max_enemies_at_level = 0
        self.start_time = 0
        self.current_level = 1
        self.current_level_start_time = 0
        self.last_spawn_time = 0
        self.cool_down_time = 3

        self.enemies: List[Enemy] = []
        if level is None:
            self.level = 1
        else:
            self.level = level

    @property
    def level(self):
        return self.current_level

    @level.setter
    def level(self, level: int = 1) -> None:
        self.current_level = level
        self.reset_level()

    # Called once per frame
    def update(self, time_in_level: float = 0.0) -> None:
        self._check_if_spawn(time_in_level)
        self._update_enemies(time_in_level)

    def clear_enemies(self) -> None:
        self.enemies = []

    def _check_if_spawn(self, time_in_level: float) -> None:
        """_summary_

        Args:
            time_in_level (int): time, in seconds, of being in level
        """
        if self.current_level > 0:
            if self._time_to_spawn(time_in_level):
                new_enemy = Enemy(shape=self.grid_shape)
                self._place_offstage_and_enter(new_enemy, time_in_level)
                self.enemies.append(new_enemy)

    def _update_enemies(self, time_in_level: float) -> None:
        remaining = []
        for enemy in self.enemies:
            enemy.update(time_in_level)
            enemy.apply_fade(time_in_level)
            if time_in_level >= enemy.next_move_at and not enemy.moving and not enemy.has_left_grid:
                moved = enemy.move_adjacent_or_leave(time_in_level)
                if moved:
                    if not enemy.leaving:
                        enemy.schedule_next_move(time_in_level)
            if enemy.has_left_grid:
                continue

            remaining.append(enemy)
        self.enemies = remaining

    def _time_to_spawn(self, time_in_level: float) -> bool:
        in_cool_down = (time_in_level - self.last_spawn_time) > self.cool_down_time

        if in_cool_down and len(self.enemies) < self.max_enemies_at_level:
            self.last_spawn_time = time_in_level
            return True
        else:
            return False

    def reset_level(self) -> None:
        """Reset level enemies, level_start_time"""
        rule = self._get_spawn_rule(self.current_level)
        self.max_enemies_at_level = rule["max_enemies"]
        self.cool_down_time = rule["cooldown"]
        self.last_spawn_time = -(self.cool_down_time + 1)  # allow immediate spawn if desired
        self.enemies = []

    def _get_spawn_rule(self, level: int) -> dict[str, int]:
        # Look up per-level rule; fall back to default or computed rule
        rule = self.spawn_rules.get(level)
        if rule is None:
            rule = self.spawn_rules.get("default")
        if rule is None:
            # fallback to prior behavior
            return {"max_enemies": level // 3, "cooldown": 3}
        return rule

    def _place_on_random_perimeter_cell(self, enemy: Enemy) -> None:
        rows, cols = self.grid_shape
        perimeter_cells = []
        # top and bottom rows
        for c in range(cols):
            perimeter_cells.append((0, c))
            perimeter_cells.append((rows - 1, c))
        # left and right columns (excluding corners already added)
        for r in range(1, rows - 1):
            perimeter_cells.append((r, 0))
            perimeter_cells.append((r, cols - 1))

        if not perimeter_cells:
            return
        row, col = random.choice(perimeter_cells)
        enemy.set_grid_position(row=row, col=col)

    def _place_offstage_and_enter(self, enemy: Enemy, time_in_level: float) -> None:
        """Spawn enemy just off-grid and animate entry onto a random perimeter cell."""
        rows, cols = self.grid_shape
        perimeter_cells = []
        for c in range(cols):
            perimeter_cells.append((0, c))
            perimeter_cells.append((rows - 1, c))
        for r in range(1, rows - 1):
            perimeter_cells.append((r, 0))
            perimeter_cells.append((r, cols - 1))

        if not perimeter_cells:
            return

        dest_row, dest_col = random.choice(perimeter_cells)
        start_row, start_col = dest_row, dest_col
        if dest_row == 0:
            start_row = -1
        elif dest_row == rows - 1:
            start_row = rows
        elif dest_col == 0:
            start_col = -1
        elif dest_col == cols - 1:
            start_col = cols

        enemy.set_position_at_cell(row=start_row, col=start_col)
        enemy.spawn_time = time_in_level
        enemy.entered = True  # allow fade-in
        enemy.image.set_alpha(0)
        enemy._start_move(dest_row=dest_row, dest_col=dest_col, now_sec=time_in_level, leaving=False)
        enemy.schedule_next_move(time_in_level + Enemy.MOVE_DURATION)
