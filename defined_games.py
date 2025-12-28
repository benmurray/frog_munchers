import enum
import numpy as np


MAX_INT = np.iinfo(int).max


class GameType(enum.Enum):
    """These need to be the display_names of the possible games"""

    Odds = 1
    Evens = 2
    Multiples = 3
    Factors = 4
    Primes = 5


def get_game(game_type: "GameType", level: int = 1) -> "Game":
    if game_type == GameType.Odds:
        return Odds(level=level)
    elif game_type == GameType.Evens:
        return Evens(level=level)
    elif game_type == GameType.Multiples:
        return Multiples(level=2)
    elif game_type == GameType.Factors:
        return Factors(level=1)
    elif game_type == GameType.Primes:
        return Primes(level=1)


class Game:
    """
    Parent class for all games
    """

    def __init__(self, level: int = 1):
        self.grid = self.generate_grid(level=level)
        self.current_value = -999
        self.gameover = False
        self.level = level
        self.last_level = 12
        self.lives = 3
        self.score = 0
        self.starting_level = level

    @property
    def level_title(self) -> str:
        raise NotImplementedError

    @property
    def message(self) -> str:
        raise NotImplementedError

    def set_lives(self, lives: int) -> None:
        self.lives = lives

    def start_over(self, lives: int, level: int | None = None) -> None:
        if level is None:
            self.level = self.starting_level
        else:
            self.level = level
        self.lives = lives

    def is_cell_populated(self, x: int, y: int) -> bool:
        if self.grid[y, x] == MAX_INT:
            return False
        else:
            return True

    def munch_number(self, x: int, y: int) -> bool:
        """Hero eats number, so set that cell value to BOGUS Value so its not displayed"""
        self.current_value = self.grid[y, x]
        self.grid[y, x] = MAX_INT
        # if not self.is_value_valid() or self.did_i_win():
        if self.is_value_valid():
            self.score += 5
            return True
        else:
            self.lives -= 1
            if self.lives == 0:
                self.gameover = True
            return False

    def is_value_valid(self) -> bool:
        raise NotImplementedError

    def start_next_level(self) -> None:
        # if self.level > self.last_level:
        if self.level == 12:
            self.gameover = True
        # You Won completely
        else:
            self.level += 1
            self.grid = self.generate_grid(level=self.level)

    @staticmethod
    def generate_grid(rows: int = 5, cols: int = 6, level: int = 1):
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 1
        high = (10 * level) + 1
        return np.random.randint(low, high, size=(rows, cols))


class Evens(Game):
    """
    Class to hold logic for game for playing evens
    """

    def __init__(self, level: int = 1):
        super(Evens, self).__init__(level)
        self.display_name = "Evens"
        self.description = "Find the even numbers! (Numbers divisible by 2)"

    @property
    def level_title(self) -> str:
        return "Evens"

    @property
    def message(self) -> str:
        return f"Look again! {self.current_value} is not an even number."

    def is_value_valid(self) -> bool:
        if self.current_value % 2 == 1:
            return False
        else:
            return True

    def beat_level(self) -> bool:
        """Take a game grid and check if all values left are odd"""
        are_all_odd = np.all((self.grid % 2) == 1)
        return are_all_odd


class Odds(Game):
    """
    Class to hold logic for game for playing Odds
    """

    def __init__(self, level: int = 1):
        super(Odds, self).__init__(level)
        self.display_name = "Odds"
        self.description = "Find the odds numbers! (Numbers NOT divisible by 2)"

    @property
    def level_title(self) -> str:
        return "Odds"

    @property
    def message(self) -> str:
        return f"Look again! {self.current_value} is not an odd number."

    def is_value_valid(self) -> bool:
        if self.current_value % 2 == 1:
            return True
        else:
            return False

    def beat_level(self) -> bool:
        """Take a game grid and check if all values left are even"""
        are_all_odd = np.all((self.grid[self.grid < (MAX_INT - 1)] % 2) == 0)
        return are_all_odd


class Multiples(Game):
    """
    Class to hold logic for game for playing Odds
    """

    def __init__(self, level: int = 2):
        super(Multiples, self).__init__(level)
        self.display_name = "Multiples"
        self.description = "Find Multiples of the Level!"
        self.level = level

    @property
    def level_title(self) -> str:
        if self.level is not None:
            return f"{self.display_name} of {self.level}"
        else:
            return self.display_name

    @property
    def message(self) -> str:
        return f"Look again! {self.current_value} is not a multiple of {self.level}."

    def is_value_valid(self) -> bool:
        if self.current_value % self.level == 0:
            return True
        else:
            return False

    def beat_level(self) -> bool:
        """Take a game grid and check if all values left are even"""
        no_more_multiples = np.all(
            (self.grid[self.grid < (MAX_INT - 1)] % self.level) != 0
        )
        return no_more_multiples

    @staticmethod
    def generate_grid(rows: int = 5, cols: int = 6, level: int = 1):
        num_right_answers = int((np.random.randint(4, 6) * 0.1) * (rows * cols))
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 1
        high = (12 * level) + 1
        grid = np.random.randint(low, high, size=(rows * cols))

        if rows * cols - np.count_nonzero(grid % level) < num_right_answers:
            current_right_answers = rows * cols - np.count_nonzero(grid % level)
            num_to_add = num_right_answers - current_right_answers
            while num_to_add > 0:
                random_place = np.random.randint(0, rows * cols)
                if grid[random_place] % level != 0:
                    multiple_of_level = np.random.randint(1, 12) * level
                    grid[random_place] = multiple_of_level
                    num_to_add = num_to_add - 1

        return grid.reshape((rows, cols))


class Factors(Game):
    """
    Class to hold logic for game for playing Factors
    """

    def __init__(self, level: int = 2):
        super(Factors, self).__init__(level)
        self.display_name = "Factors"
        self.description = "Find Factors of the Level!"
        self.level = level

    @property
    def level_title(self) -> str:
        if self.level is not None:
            return f"{self.display_name} of {self.level * 12}"
        else:
            return self.display_name

    @property
    def message(self) -> str:
        return f"Look again! {self.current_value} is not a factor of {self.level * 12}."

    def is_value_valid(self) -> bool:
        if self.current_value in self.primes:
            return True
        else:
            return False

    def beat_level(self) -> bool:
        """Take a game grid and check if all values left are even"""
        no_more_multiples = np.all(
            ((self.level * 12) % self.grid[self.grid < (MAX_INT - 1)]) != 0
        )
        return no_more_multiples

    @staticmethod
    def generate_grid(rows: int = 5, cols: int = 6, level: int = 1):
        num_right_answers = int((np.random.randint(4, 6) * 0.1) * (rows * cols))
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 1
        high = (12 * level) + 1  
        grid = np.random.randint(low, high, size=(rows * cols))

        if rows * cols - np.count_nonzero(grid % level) < num_right_answers:
            current_right_answers = rows * cols - np.count_nonzero(grid % level)
            num_to_add = num_right_answers - current_right_answers
            while num_to_add > 0:
                random_place = np.random.randint(0, rows * cols)
                if grid[random_place] % level != 0:
                    multiple_of_level = np.random.randint(1, 12) * level
                    grid[random_place] = multiple_of_level
                    num_to_add = num_to_add - 1

        return grid.reshape((rows, cols))


class Primes(Game):
    """
    Class to hold logic for game for playing Primes
    """

    def __init__(self, level: int = 2):
        super(Primes, self).__init__(level)
        self.display_name = "Primes"
        self.description = "Find Prime Numbers!"
        self.primes = [
                2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
                139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
                223, 227, 229, 233, 239, 241, 251
        ]

    @property
    def level_title(self) -> str:
        return "Primes"

    @property
    def message(self) -> str:
        return f"Look again! {self.current_value} is not a prime number."

    def is_value_valid(self) -> bool:
        if self.current_value in self.primes:
            return True
        else:
            return False 

    def beat_level(self) -> bool:
        """Take a game grid and check if all values left are odd"""
        for value in self.grid[self.grid < (MAX_INT - 1)]:
            if value in self.primes:
                return False

        # no primes found
        return True

    @staticmethod
    def generate_grid(rows: int = 5, cols: int = 6, level: int = 1):
        primes = [
                2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
                139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
                223, 227, 229, 233, 239, 241, 251
        ]

        num_right_answers = int((np.random.randint(4, 6) * 0.1) * (rows * cols))
        if rows <= 0:
            rows = 5
        if cols <= 0:
            cols = 6
        low = 1
        high = (12 * level) + 1  
        grid = np.random.randint(low, high, size=(rows * cols))

        if rows * cols - np.count_nonzero(grid % level) < num_right_answers:
            current_right_answers = rows * cols - np.count_nonzero(grid % level)
            num_to_add = num_right_answers - current_right_answers
            while num_to_add > 0:
                random_place = np.random.randint(0, rows * cols)
                if grid[random_place] not in primes:
                    multiple_of_level = 12 * level

                    random_prime = primes[np.random.randint(0, len(primes))]
                    while random_prime > multiple_of_level:
                        random_prime = primes[np.random.randint(0, len(primes))]
                    grid[random_place] = random_prime
                    num_to_add = num_to_add - 1

        return grid.reshape((rows, cols))
