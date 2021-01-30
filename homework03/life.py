import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
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

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        matrix = []

        for y in range(self.rows):

            row = []
            for x in range(self.cols):
                if randomize is True:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)

            matrix.append(row)

        return matrix

    def get_neighbours(self, cell: Cell) -> Cells:
        neigbours = []

        start_row = None
        end_row = None
        start_column = None
        end_column = None

        if cell[0] == 0:
            start_row = cell[0]
        else:
            start_row = cell[0] - 1

        if cell[0] == self.rows - 1:
            end_row = cell[0]
        else:
            end_row = cell[0] + 1

        if cell[1] == 0:
            start_column = cell[1]
        else:
            start_column = cell[1] - 1

        if cell[1] == self.cols - 1:
            end_column = cell[1]
        else:
            end_column = cell[1] + 1

        for i in range(start_row, end_row + 1):
            for j in range(start_column, end_column + 1):
                if i != cell[0] or j != cell[1]:
                    neigbours.append(self.curr_generation[i][j])

        return neigbours

    def get_next_generation(self) -> Grid:
        next = self.create_grid()

        for i in range(self.rows):
            for j in range(self.cols):

                neighbours = self.get_neighbours((i, j))

                if sum(neighbours) < 2:
                    next[i][j] = 0

                elif sum(neighbours) > 3:
                    next[i][j] = 0

                elif sum(neighbours) == 3:
                    next[i][j] = 1

                else:
                    next[i][j] = self.curr_generation[i][j]
        return next

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = copy.deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """

        data = None
        matrix = []

        with open(filename, "r") as file:
            data = file.readlines()

        for line in data:
            row = []
            chars = line.split("")
            for char in chars:
                row.append(int(char))

            matrix.append(row)

        rows_count = len(matrix)
        columns_count = len(matrix[0]) if (rows_count > 0) else 0

        life = GameOfLife(size=(rows_count, columns_count))
        life.curr_generation = matrix

        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        doc = open(filename, "w")
        for row in self.curr_generation:
            for col in row:
                doc.write(str(col))
            doc.write("\n")
        doc.close()
