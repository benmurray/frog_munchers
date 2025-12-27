from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


TITLE = 'Frog Munchers!'
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BOARD_WIDTH = 900
BOARD_HEIGHT = 500

FRAME_RATE = 60

# Farrar Frog Green
GREEN = "#12581a"
GREEN2 = "#006118"

# Enemy spawn tuning per level. Adjust max enemies and spawn cooldown (seconds) here.
# If a level is missing, default rules are used.
ENEMY_SPAWN_RULES = {
    "default": {"max_enemies": 0, "cooldown": 3},
    1: {"max_enemies": 1, "cooldown": 1},
    2: {"max_enemies": 1, "cooldown": 4},
    3: {"max_enemies": 1, "cooldown": 3},
    4: {"max_enemies": 2, "cooldown": 3},
    5: {"max_enemies": 2, "cooldown": 2},
}