"""
Conway's Game Of Life business logic implementation
"""
import argparse
import pathlib
import random
import typing as tp
from copy import deepcopy

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


history: tp.List[Grid] = []


class GameOfLife:
    """
    Business logic class
    """

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        # Add generation to history
        history.append(self.curr_generation)

    def is_alive(self, cell: Cell) -> bool:
        """
        Checks if a cell is alive
        """
        return bool(self.curr_generation[cell[0]][cell[1]])

    def _is_a_cell(self, cell: Cell) -> bool:
        """
        Checks a cell for coordinate validity
        """
        return 0 <= cell[0] < len(self.curr_generation) and 0 <= cell[1] < len(
            self.curr_generation[0]
        )

    def set_cell_value(self, cell: Cell, value: int) -> None:
        """
        Assigns a value to a cell
        """
        if not value in (0, 1):
            raise ValueError("Illegal value, should be 0 or 1")
        self.curr_generation[cell[0]][cell[1]] = value

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Generates a grid
        """
        return [
            [random.randint(0, 1) if randomize else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Gets neighbor positions for a cell
        """
        neighbors = []
        shifts = (
            (i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]
        )  # possible shifts for neighbors
        for x_c, y_c in shifts:  # 9 possible cells in a quadrant
            if (x_c, y_c) == (0, 0):  # except the one we check
                continue

            row, col = cell[0] + x_c, cell[1] + y_c
            if self._is_a_cell((row, col)):
                neighbors.append(int(self.is_alive((row, col))))

        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Gets next generation for self.curr_generation
        """
        out = deepcopy(
            self.curr_generation
        )  # because python assignments create references and do not copy values
        # https://docs.python.org/3/faq/programming.html#how-do-i-copy-an-object-in-python

        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[i])):
                neighbors = self.get_neighbours((i, j))
                alive = sum(neighbors)

                if self.is_alive((i, j)):
                    if 2 <= alive <= 3:  # supports life
                        out[i][j] = 1
                    else:  # either no food or overpopulated
                        out[i][j] = 0
                elif alive == 3:  # breathe life into a dead cell near some alive cells
                    out[i][j] = 1

        return out

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation[:]
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        history.append(self.curr_generation)

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if not self.max_generations:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for state in history:
            if self.curr_generation == state:
                return False
        # return self.prev_generation != self.curr_generation
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        start_gen = []
        with open(filename, "r") as game_file:
            for line in game_file.readlines():
                if not line == "\n":  # skip trailing newline
                    start_gen.append([int(i) for i in line if i in (0, 1)])

        size = len(start_gen), len(start_gen[0])
        game = GameOfLife(size=size, randomize=False)
        game.curr_generation = start_gen
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as game_file:
            for row in self.curr_generation:
                line = "".join([str(i) for i in row])
                game_file.write(f"{line}\n")


def get_args():
    """
    Parses args and returns a corresponding namespace
    """
    argparser = argparse.ArgumentParser(description="Launch Game of Life, GUI version")
    argparser.add_argument(
        "--rows",
        dest="rows",
        action="store",
        default=10,
        type=int,
        help="Set number of rows (default: 10)",
    )
    argparser.add_argument(
        "--cols",
        dest="cols",
        action="store",
        default=10,
        type=int,
        help="Set number of columns (default: 10)",
    )
    argparser.add_argument(
        "--max-generations",
        dest="max_gens",
        action="store",
        default=float("inf"),
        type=float,
        help="Set generations limit (default: no limit)",
    )
    argparser.add_argument(
        "--path",
        dest="load_path",
        action="store",
        default=None,
        type=pathlib.Path,
        help="Load state from a file",
    )
    argparser.add_argument(
        "--width",
        dest="width",
        action="store",
        default=640,
        type=int,
        help="Set width (default: 640)",
    )
    argparser.add_argument(
        "--height",
        dest="height",
        action="store",
        default=480,
        type=int,
        help="Set height (default: 480)",
    )
    argparser.add_argument(
        "--cell_size",
        dest="cell_size",
        action="store",
        default=10,
        type=int,
        help="Set cell size (default: 10)",
    )
    arguments = argparser.parse_args()
    return arguments
