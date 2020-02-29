

class Evens:
    """
    Class to hold logic for game for playing evens
    """
    def __init__(self, level=1):
        self.grid = self.generate_grid(level=1)
        self.value = -999
        self.message = f"Look again! {self.value} is not an even number."

    @staticmethod
    def generate_grid(rows=5, cols=6, level=1):
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 0
        high = (10 * level) + 1
        return np.random.randint(low, high, size(rows, cols))

    @staticmethod
    def is_value_valid(value):
        if value % 2 == 0:
            return true

    def consume(self, x, y):
        """Hero eats number, so set that cell value to BOGUS Value so its not displayed"""
        self.grid[y, x] = -1

    def did_i_win(self):
        """Take a game grid and check if all values left are odd"""
        are_any_odd = np.any((self.grid % 2) == 1)
        return are_any_odd


