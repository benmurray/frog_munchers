import numpy as np
import enum


class GameType(enum.Enum):
    """These need to be the display_names of the possible games"""
    Odds = 1
    Evens = 2
    Multiples = 3
    Factors = 4


def get_game(game_type, level=1):
    if game_type == GameType.Odds:
        return Odds(level=level)
    elif game_type == GameType.Evens:
        return Evens(level=level)


class Evens:
    """
    Class to hold logic for game for playing evens
    """

    def __init__(self, level=1):
        self.grid = self.generate_grid(level=level)
        self.current_value = -999
        self.gameover = False
        self.level = level
        self.score = 0
        self.display_name = "Evens"
        self.description = "Find the even numbers! (Numbers divisible by 2)"

    @property
    def level_title(self):
        return f"Evens"

    @property
    def message(self):
        return f"Look again! {self.current_value} is not an even number."

    @staticmethod
    def generate_grid(rows=5, cols=6, level=1):
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 0
        high = (10 * level) + 1
        return np.random.randint(low, high, size=(rows, cols))

    def is_value_valid(self):
        if self.current_value % 2 == 1:
            return False
        else:
            return True

    def munch_number(self, x, y):
        """Hero eats number, so set that cell value to BOGUS Value so its not displayed"""
        self.current_value = self.grid[y, x]
        self.grid[y, x] = -1
        # if not self.is_value_valid() or self.did_i_win():
        if self.is_value_valid():
            self.score += 5
        else:
            self.gameover = True

    def beat_level(self):
        """Take a game grid and check if all values left are odd"""
        are_all_odd = np.all((self.grid % 2) == 1)
        return are_all_odd

    def start_next_level(self):
        if self.level == 12:
            self.gameover = True
            # You Won completely
        else:
            self.level += 1
            self.grid = self.generate_grid(level=self.level)


class Odds:
    """
    Class to hold logic for game for playing Odds
    """

    def __init__(self, level=1):
        self.grid = self.generate_grid(level=level)
        self.current_value = -999
        self.gameover = False
        self.level = level
        self.score = 0
        self.display_name = "Odds"
        self.description = "Find the odds numbers! (Numbers NOT divisible by 2)"

    @property
    def level_title(self):
        return f"Odds"

    @property
    def message(self):
        return f"Look again! {self.current_value} is not an odd number."

    @staticmethod
    def generate_grid(rows=5, cols=6, level=1):
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 0
        high = (10 * level) + 1
        return np.random.randint(low, high, size=(rows, cols))

    def is_value_valid(self):
        if self.current_value % 2 == 1:
            return True
        else:
            return False

    def munch_number(self, x, y):
        """Hero eats number, so set that cell value to BOGUS Value so its not displayed"""
        self.current_value = self.grid[y, x]
        self.grid[y, x] = -1
        # if not self.is_value_valid() or self.did_i_win():
        if self.is_value_valid():
            self.score += 5
        else:
            self.gameover = True

    def beat_level(self):
        """Take a game grid and check if all values left are even"""
        are_all_even = np.all((self.grid % 2) == 0)
        return are_all_even

    def start_next_level(self):
        if self.level == 12:
            self.gameover = True
            # You Won completely
        else:
            self.level += 1
            self.grid = self.generate_grid(level=self.level)
