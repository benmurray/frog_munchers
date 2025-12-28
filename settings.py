import os
import sys
from pathlib import Path
from enum import Enum

# Resolve base path for assets (handles PyInstaller _MEIPASS) and a writable state dir
BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ASSETS_DIR = BASE_DIR / "assets"
STATE_DIR = Path(os.environ.get("FROG_MUNCHERS_STATE_DIR", Path.home() / ".frog_munchers"))


def asset_path(*parts: str) -> Path:
    return ASSETS_DIR.joinpath(*parts)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


TITLE = 'Farrar Frog Munchers!'
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BOARD_WIDTH = 900
BOARD_HEIGHT = 500

FRAME_RATE = 60
# Where high scores are stored (writable, outside packaged assets)
HIGH_SCORE_FILE = STATE_DIR / "high_scores.pkl"

# Farrar Frog Green
GREEN = "#12581a"
GREEN2 = "#006118"

# Enemy spawn tuning per level. Adjust max enemies and spawn cooldown (seconds) here.
# If a level is missing, default rules are used.
ENEMY_SPAWN_RULES = {
    # difficulty: 1=green, 2=green+purple, 3=green+purple+red, 4=all (blue added)
    "default": {"max_enemies": 3, "cooldown": 5, "difficulty": 4},
    1: {"max_enemies": 0, "cooldown": 1, "difficulty": 1},
    2: {"max_enemies": 0, "cooldown": 4, "difficulty": 1},
    3: {"max_enemies": 1, "cooldown": 3, "difficulty": 1},
    4: {"max_enemies": 1, "cooldown": 3, "difficulty": 1},
    5: {"max_enemies": 1, "cooldown": 2, "difficulty": 2},
    6: {"max_enemies": 1, "cooldown": 1, "difficulty": 2},
    7: {"max_enemies": 2, "cooldown": 4, "difficulty": 2},
    8: {"max_enemies": 2, "cooldown": 3, "difficulty": 3},
    9: {"max_enemies": 2, "cooldown": 3, "difficulty": 3},
    10: {"max_enemies": 2, "cooldown": 2, "difficulty": 4},
}
