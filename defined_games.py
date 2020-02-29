import numpy as np


class Evens:
    """
    Class to hold logic for game for playing evens
    """
    def __init__(self, level=1):
        self.grid = self.generate_grid(level=1)
        self.current_value = -999
        self.gameover = False

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
        if not self.is_value_valid() or self.did_i_win():
            self.gameover = True

    def did_i_win(self):
        """Take a game grid and check if all values left are odd"""
        are_all_odd = np.all((self.grid % 2) == 1)
        return are_all_odd


